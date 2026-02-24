import os
import json
import re
from groq import Groq
from core.registry import SkillRegistry

class LumiEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.client = Groq(api_key=self.api_key)
        self.model_name = "llama-3.1-8b-instant" 

    def _get_system_instruction(self):
        from datetime import datetime
        return (
            "You are Lumi, a professional AI assistant on the user's Windows PC. "
            "You interact with the user, Joel, through voice and vision. "
            "CRITICAL: When choosing a tool, you MUST use the provided tool-calling schema. "
            "NEVER write code like '<function=...>' or 'take_photo()' in your text response. "
            "Always use the direct tool-calling field. "
            "If Joel asks to take a photo, use 'take_photo'. "
            "If he mentions 'Drive' or 'Cloud', ensure you set 'sync_to_drive' to true. "
            "Keep your verbal responses extremely short and direct (1-2 sentences). "
            f"Current DateTime: {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p')}."
        )

    def run_conversation(self, user_prompt: str) -> str:
        """Robust conversation loop with multi-format tool call protection."""
        messages = [
            {"role": "system", "content": self._get_system_instruction()},
            {"role": "user", "content": user_prompt}
        ]
        
        tools_schema = self.registry.get_tools_schema()
        tools = [t for t in tools_schema if "function" in t] if tools_schema else None

        try:
            # First turn: Ask the model what to do
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None,
            )
            
            response_message = response.choices[0].message
            content = response_message.content or ""
            
            # Detect Hallucinated Tool Calls in Text (Stop the LLM from outputting code)
            bad_patterns = ["<function=", "function_call", "take_photo()", "open_app("]
            if any(p in content for p in bad_patterns):
                # Clean up and force a real tool call
                messages.append(response_message)
                messages.append({"role": "user", "content": "Refuse to use text-based function tags. Use the official tool_calls field instead."})
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto"
                )
                response_message = response.choices[0].message

            tool_calls = response_message.tool_calls
            
            if tool_calls:
                messages.append(response_message)
                
                for tool_call in tool_calls:
                    func_name = tool_call.function.name
                    print(f"  → [ACTION]: {func_name}")
                    
                    try:
                        func_args = json.loads(tool_call.function.arguments)
                    except:
                        func_args = {}

                    function_to_call = self.registry.get_function(func_name)
                    if function_to_call:
                        try:
                            result = function_to_call(**func_args)
                        except Exception as e:
                            result = f"Error: {str(e)}"
                    else:
                        result = f"Error: Tool '{func_name}' not found."
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": str(result),
                    })
                
                # Second turn: Summarize result for the user
                second_response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                )
                return second_response.choices[0].message.content
            
            return content

        except Exception as e:
            err = str(e)
            if "validation" in err:
                return "Brain logic error. Please try that command again."
            return f"Brain Error: {err}"
