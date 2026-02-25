import os
import json
import re
import time
import hashlib
from groq import Groq
from core.registry import SkillRegistry

class LumiEngine:
    def __init__(self, registry: SkillRegistry):
        self.registry = registry
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        # Use OpenRouter's GPT-4o model for chat and tasks
        self.model_name = "openai/gpt-4o"
        
        # OpenRouter config (user-provided key stored in .env)
        self.openrouter_key = os.environ.get("OPENROUTER_API_KEY", "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")
        # Force OpenRouter as the only engine
        self.default_to_openrouter = True
        self.use_openrouter_backup = False
        
        self.max_retries = 3
        self.base_wait_time = 1  # seconds
        self.response_cache = {}  # Simple in-memory cache
        self.cache_ttl = 300  # 5 minutes cache
        self.groq_failed = False  # Track if Groq is failing
        
        self.system_instruction = (
            "You are LUMI, a powerful Windows AI assistant designed for Joel. Your personality is friendly, efficient, and always helpful. "
            "You have advanced control over Windows system functions including: "
            "- Brightness control (increase, decrease, set to specific level) "
            "- Volume control (increase, decrease, mute, unmute, set to specific level) "
            "- Battery status monitoring "
            "- App launching and management "
            "- YouTube and web search integration "
            "- System information (CPU, memory, battery status) "
            "- n8n workflow automation via webhook (save calendars, reminders, emails, tasks) "
            "Always be friendly and natural in responses. When performing actions, use the appropriate tools. "
            "When using tools, output VALID JSON arguments only in the format expected by the API. "
            "Do NOT output the tool call as XML or with an equals sign. "
            "Just use the standard tool calling format provided by the API."
        )

    def _api_call_with_retry(self, **kwargs):
        """Make API call with exponential backoff retry logic"""
        # If configured to use OpenRouter by default, try it first
        if self.default_to_openrouter and self.use_openrouter_backup:
            try:
                return self._openrouter_api_call(**kwargs)
            except Exception as e:
                print(f"DEBUG: OpenRouter primary call failed: {str(e)[:120]}, falling back to Groq")

        # Otherwise or if OpenRouter failed, try Groq with retries
        last_exc = None
        for attempt in range(self.max_retries):
            try:
                return self.client.chat.completions.create(**kwargs)
            except Exception as e:
                last_exc = e
                error_str = str(e)
                # Check for rate limit on Groq
                if "429" in error_str or "rate limit" in error_str.lower():
                    if attempt < self.max_retries - 1:
                        wait_time = self.base_wait_time * (2 ** attempt)
                        print(f"DEBUG: Groq rate limit hit. Retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"DEBUG: Groq exhausted after {self.max_retries} attempts.")
                        break
                else:
                    # non-rate-limit error -> break and try OpenRouter if available
                    print(f"DEBUG: Groq error: {error_str[:120]}")
                    break

        # If we reach here, Groq failed; try OpenRouter as fallback
        if self.use_openrouter_backup:
            try:
                return self._openrouter_api_call(**kwargs)
            except Exception as e:
                print(f"ERROR: Both Groq and OpenRouter calls failed: {str(e)[:200]}")
                raise last_exc or e
        
        raise last_exc or Exception("API call failed")

    def _openrouter_api_call(self, **kwargs):
        """Make API call using OpenRouter as fallback"""
        try:
            from openai import OpenAI
        except ImportError:
            print("ERROR: OpenAI library not installed. Install with: pip install openai")
            raise Exception("OpenRouter unavailable - OpenAI library required")
        
        try:
            client = OpenAI(
                api_key=self.openrouter_key,
                base_url="https://openrouter.io/api/v1"
            )
            
            # Always use GPT-4o for chat and tasks
            model = kwargs.get('model', self.model_name)
            kwargs['model'] = model
            print(f"DEBUG: Using OpenRouter model: {model}")
            response = client.chat.completions.create(**kwargs)
            print("DEBUG: OpenRouter API call successful!")
            return response
            
        except Exception as e:
            print(f"ERROR: OpenRouter API call failed: {str(e)[:100]}")
            raise e

    def _get_cache_key(self, user_prompt: str) -> str:
        """Generate cache key from user prompt"""
        return hashlib.md5(user_prompt.lower().strip().encode()).hexdigest()

    def _check_cache(self, user_prompt: str):
        """Check if response is cached"""
        cache_key = self._get_cache_key(user_prompt)
        if cache_key in self.response_cache:
            cached_time, cached_response = self.response_cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                print(f"DEBUG: Cache HIT for: {user_prompt[:50]}")
                return cached_response
            else:
                del self.response_cache[cache_key]
        return None

    def _get_local_response(self, user_prompt: str) -> str:
        """Provide smart local responses for common queries without API calls"""
        prompt_lower = user_prompt.lower().strip()
        
        # Common greetings
        greetings = ["hello", "hi", "hey", "what's up", "howdy"]
        if any(g in prompt_lower for g in greetings):
            if "are you" in prompt_lower or "how are" in prompt_lower:
                return "I'm doing great, thanks for asking! I'm ready to help you with anything. How can I assist you today?"
            return "Hey there! I'm LUMI, your Windows AI assistant. What can I do for you?"
        
        # Common time/date queries
        if "time" in prompt_lower or "what time" in prompt_lower:
            return "I'll check the time for you. Let me fetch the current time."
        if "date" in prompt_lower or "what date" in prompt_lower:
            return "Let me get today's date for you."
        
        # System info queries
        if "battery" in prompt_lower or "charge" in prompt_lower:
            return "Let me check your battery status for you."
        if "storage" in prompt_lower or "disk" in prompt_lower or "space" in prompt_lower:
            return "I'll check your storage information."
        if "system" in prompt_lower or "computer" in prompt_lower:
            return "Let me gather your system information."
        
        # Screenshot/Camera
        if "screenshot" in prompt_lower or "screen" in prompt_lower:
            return "I'll capture a screenshot for you and save it to your Desktop folder."
        if "photo" in prompt_lower or "picture" in prompt_lower or "camera" in prompt_lower:
            return "I'll take a photo using your camera and save it to your Desktop folder."
        
        # Volume/Brightness
        if "volume" in prompt_lower or "sound" in prompt_lower:
            return "I'll adjust your volume for you."
        if "brightness" in prompt_lower or "bright" in prompt_lower:
            return "I'll adjust your screen brightness."
        
        # Web/Search
        if "search" in prompt_lower or "google" in prompt_lower:
            return "I'll search the web for you."
        if "youtube" in prompt_lower or "video" in prompt_lower:
            return "I'll open YouTube for you."
        
        # Email
        if "email" in prompt_lower or "mail" in prompt_lower:
            return "I can help you with email. What would you like to do?"
        
        # Calendar
        if "calendar" in prompt_lower or "event" in prompt_lower or "remind" in prompt_lower:
            return "I'll help you with calendar events and reminders."
        
        return None  # Fall through to API call

    def _is_local_query(self, user_prompt: str) -> bool:
        """Check if query can be answered locally"""
        return self._get_local_response(user_prompt) is not None




    def run_conversation(self, user_prompt: str) -> str:
        # Check cache first for non-tool requests
        cached_response = self._check_cache(user_prompt)
        if cached_response:
            return cached_response
        
        messages = [
            {"role": "system", "content": self.system_instruction},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            tools_schema = self.registry.get_tools_schema()
            
            completion_kwargs = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": 1000
            }
            
            if tools_schema:
                completion_kwargs["tools"] = tools_schema
                completion_kwargs["tool_choice"] = "auto"
            
            # Use retry logic for first API call
            response = self._api_call_with_retry(**completion_kwargs)
            
        except Exception as e:
            # Detailed error handling
            error_str = str(e)
            print(f"ERROR: First API call failed: {error_str[:200]}")
            
            # Try local response first on rate limit
            if "429" in error_str or "rate limit" in error_str.lower():
                print(f"DEBUG: API Rate limited, using local response")
                local_response = self._get_local_response(user_prompt)
                if local_response:
                    return local_response
                return "I'm sorry, I'm having trouble connecting to my AI servers right now, but I'm still here to help! Please ask me anything, and I'll do my best to assist you or provide a smart answer."
            
            # Try to recover from tool_use_failed errors
            if "tool_use_failed" in error_str:
                try:
                    match = re.search(r"<function=(\w+)(?:.*?)(\{.*?\})", error_str)
                    if match:
                        func_name = match.group(1)
                        func_args_str = match.group(2)
                        print(f"DEBUG: Attempting recovery of failed tool: {func_name}")
                        
                        function_to_call = self.registry.get_function(func_name)
                        if function_to_call:
                            try:
                                args = json.loads(func_args_str)
                                res = function_to_call(**args)
                                return str(res)
                            except Exception as exec_e:
                                print(f"DEBUG: Recovery failed: {exec_e}")
                                return f"Task executed but had an issue: {exec_e}"
                except Exception as parse_e:
                    print(f"DEBUG: Could not parse recovery: {parse_e}")
            
            # Return helpful message
            return "I'm here and ready to help! If my AI servers are slow, just ask again or try a different question. I can still assist with Windows tasks, system info, and more."

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # CASE 1: AI wants to use a tool (Action)
        if tool_calls:
            print("DEBUG: Executing Tool...")
            messages.append(response_message)

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                print(f"DEBUG: AI attempting to call: {function_name}")
                
                function_to_call = self.registry.get_function(function_name)
                
                if not function_to_call:
                    res = f"Tool '{function_name}' not available"
                    print(f"DEBUG: Tool {function_name} not found")
                else:
                    try:
                        # Handle tool arguments properly
                        if hasattr(tool_call.function, 'arguments'):
                            if isinstance(tool_call.function.arguments, str):
                                function_args = json.loads(tool_call.function.arguments)
                            else:
                                function_args = tool_call.function.arguments
                        else:
                            function_args = {}
                        
                        if function_args is None:
                            function_args = {}
                        
                        print(f"DEBUG: Executing {function_name}")
                        res = function_to_call(**function_args)
                        print(f"DEBUG: Tool Output: {str(res)[:150]}")
                    except Exception as e:
                        res = f"Error executing tool: {str(e)[:100]}"
                        print(f"DEBUG: Tool Execution Error: {e}")

                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(res),
                    }
                )
            
            # Get final response after tool execution with retry
            try:
                second_response = self._api_call_with_retry(
                    model=self.model_name,
                    messages=messages,
                    max_tokens=500
                )
                result = second_response.choices[0].message.content
                return result
            except Exception as second_error:
                print(f"ERROR: Second API call failed: {second_error}")
                error_str = str(second_error)
                
                # Check if it's rate limit and use local response
                if "429" in error_str or "rate limit" in error_str.lower():
                    tool_results = [msg.get("content", "") for msg in messages if msg.get("role") == "tool"]
                    if tool_results:
                        # Return successful tool execution result  
                        results_text = ' '.join([r for r in tool_results if r and "error" not in r.lower()][:100])
                        return f"Done! {results_text}" if results_text else "Task executed successfully!"
                    return "Operation completed. If you need more details, please ask."
                
                # Fallback: return tool result summary
                tool_results = [msg.get("content", "") for msg in messages if msg.get("role") == "tool"]
                if tool_results:
                    return f"Done! {' '.join([r for r in tool_results if r][:100])}"
                else:
                    return "Task processed. I'm having trouble getting details, but your request was handled."
        
        # CASE 2: AI just wants to chat
        else:
            result = response_message.content
            # Cache simple chat responses
            self._cache_response(user_prompt, result)
            return result
