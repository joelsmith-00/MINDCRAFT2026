import os
import json
import requests
from core.registry import SkillRegistry

class LumiEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        
        # Determine provider- based on available keys
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY")
        self.gemini_key = os.environ.get("GEMINI_API_KEY")
        
        if self.openrouter_key:
            self.provider = "openrouter"
            self.api_key = self.openrouter_key.strip()
            self.model_name = "openai/gpt-3.5-turbo" # Stable fallback
            self.url = "https://openrouter.ai/api/v1/chat/completions"
        else:
            self.provider = "gemini"
            self.api_key = self.gemini_key.strip() if self.gemini_key else "AIzaSyBW8ix-wT27-Fe8wf2mXtMQMbDWwDgaTE4"
            self.model_name = "gemini-1.5-flash"
            self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        
    def _get_system_instruction(self):
        from datetime import datetime
        return (
            "You are Lumi, a fast and powerful AI assistant on the user's Windows PC. "
            "You have full system access. Keep ALL responses very short — max 1-2 sentences. "
            "Be direct and concise. No filler text. The user's name is Joel. "
            f"Current DateTime: {datetime.now().strftime('%A, %B %d, %Y, %I:%M %p')}. "
            "If asked to take an action, use the tools provided."
        )

    def run_conversation(self, user_prompt: str) -> str:
        if self.provider == "openrouter":
            return self._run_openrouter(user_prompt)
        else:
            return self._run_gemini(user_prompt)

    def _run_openrouter(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": self._get_system_instruction()},
            {"role": "user", "content": user_prompt}
        ]
        
        tools = []
        tools_schema = self.registry.get_tools_schema()
        if tools_schema:
            for tool in tools_schema:
                # Convert to OpenAI tool format if necessary (though current schema seems to match)
                tools.append(tool)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/joelm/Project_JARVIS", # Recommended for OpenRouter
            "X-Title": "LUMI AI Assistant"
        }
        
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "tools": tools if tools else None,
                "tool_choice": "auto" if tools else None
            }
            
            response = requests.post(self.url, headers=headers, json=payload, timeout=20)
            res_json = response.json()
            
            if "error" in res_json:
                return f"Brain Error: {res_json['error'].get('message', 'Unknown error')}"

            choice = res_json["choices"][0]
            message = choice["message"]
            
            if message.get("tool_calls"):
                messages.append(message)
                for tool_call in message["tool_calls"]:
                    func_name = tool_call["function"]["name"]
                    func_args = json.loads(tool_call["function"]["arguments"])
                    print(f"  → Executing action: {func_name}")
                    
                    function_to_call = self.registry.get_function(func_name)
                    if function_to_call:
                        try:
                            res = function_to_call(**func_args)
                        except Exception as e:
                            res = f"Error: {e}"
                    else:
                        res = "Error: Tool not found."
                        
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": func_name,
                        "content": str(res)
                    })
                
                final_response = requests.post(self.url, headers=headers, json={
                    "model": self.model_name,
                    "messages": messages
                }, timeout=20)
                return final_response.json()["choices"][0]["message"]["content"]
            
            return message["content"]
            
        except Exception as e:
            return f"Brain connection error: {e}"

    def _run_gemini(self, user_prompt: str) -> str:
        messages = [
            {"role": "user", "parts": [{"text": f"System Instruction: {self._get_system_instruction()}\n\nUser: {user_prompt}"}]}
        ]
        
        try:
            tools_schema = self.registry.get_tools_schema()
            tools = []
            if tools_schema:
                functions = []
                for tool in tools_schema:
                    functions.append({
                        "name": tool["function"]["name"],
                        "description": tool["function"]["description"],
                        "parameters": tool["function"]["parameters"]
                    })
                tools = [{"function_declarations": functions}]

            payload = {"contents": messages, "tools": tools}
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(self.url, headers=headers, json=payload, timeout=15)
            response_json = response.json()
            
            if "error" in response_json:
                return f"Brain connection issue: {response_json['error'].get('message', 'Unknown error')}"

            candidate = response_json["candidates"][0]
            content = candidate["content"]
            parts = content.get("parts", [])
            
            tool_calls = [p.get("functionCall") for p in parts if p.get("functionCall")]
            
            if tool_calls:
                messages.append(content)
                for call in tool_calls:
                    func_name = call["name"]
                    func_args = call.get("args", {})
                    print(f"  → Executing action: {func_name}")
                    
                    function_to_call = self.registry.get_function(func_name)
                    if function_to_call:
                        try:
                            res = function_to_call(**func_args)
                        except Exception as e:
                            res = f"Error: {e}"
                    else:
                        res = "Error: Tool not found."
                    
                    messages.append({
                        "parts": [{"functionResponse": {"name": func_name, "response": {"result": str(res)}}}]
                    })
                
                final_response = requests.post(self.url, headers=headers, json={"contents": messages}, timeout=15)
                final_json = final_response.json()
                return final_json["candidates"][0]["content"]["parts"][0]["text"]
            
            return parts[0]["text"]

        except Exception as e:
            return f"Brain connection error: {e}"
