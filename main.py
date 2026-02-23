import os
import sys
import argparse
import threading 
import time
from dotenv import load_dotenv

# Load Env
load_dotenv()

def lumi_loop(pause_event, registry, args):
    """Main loop for LUMI, running in a separate thread."""
    from core.voice import speak, listen
    from core.engine import LumiEngine
    
    lumi = LumiEngine(registry)

    if args.text:
        print("LUMI: Lumi Online. Ready for command (Text Mode).")
    else:
        speak("Lumi Online. Ready for command.")

    while True:
        if pause_event.is_set():
            time.sleep(0.5)
            continue

        if args.text:
            try:
                user_query = input("YOU: ").lower()
            except EOFError:
                break
        else:
            user_query = listen()
            
        if pause_event.is_set():
            continue

        if user_query == "none" or not user_query: continue
        if "quit" in user_query or "exit" in user_query: 
            print("Shutting down LUMI...")
            if not args.text:
                speak("Shutting down.")
            break
        
        # Wake word / Command filtering
        direct_commands = [
            "open", "volume", "search", "create", "write", "read", "make",
            "who", "what", "when", "where", "how", "why", "thank", "hello",
            "weather", "temperature", "screenshot", "email", "remember",
            "forget", "detect", "photo", "time", "date", "run", "command",
            "shutdown", "restart", "sleep", "lock", "system", "battery",
            "hi", "hey", "tell", "show", "list", "find", "play", "set",
            "check", "send", "take", "please", "can", "could", "will",
            "schedule", "remind", "task", "calendar", "telegram", "n8n"
        ]
        
        is_direct = any(cmd in user_query for cmd in direct_commands)
        
        # Wake word is "lumi" now (also accept "jarvis" for backward compat)
        has_wake_word = "lumi" in user_query or "loomy" in user_query or "lumy" in user_query or "luminee" in user_query
        
        if not has_wake_word and not is_direct:
            print(f"Ignored: {user_query}")
            continue
            
        # Remove wake word from query
        clean_query = user_query
        for word in ["lumi", "loomy", "lumy", "luminee", "jarvis"]:
            clean_query = clean_query.replace(word, "").strip()
        
        if not clean_query:
            clean_query = "hello"
        
        try:
            print(f"Thinking: {clean_query}")
            response = lumi.run_conversation(clean_query)
            
            if pause_event.is_set():
                continue

            if response:
                if args.text:
                    print(f"LUMI: {response}")
                else:
                    speak(response)
        except Exception as e:
            print(f"Loop Error: {e}")
            if args.text:
                print("LUMI: System error.")
            else:
                speak("System error.")

def main():
    parser = argparse.ArgumentParser(description="LUMI AI Assistant")
    parser.add_argument("--text", action="store_true", help="Run in text mode (no voice I/O)")
    args = parser.parse_args()

    if not os.environ.get("OPENROUTER_API_KEY") and not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GROQ_API_KEY"):
        print("=" * 60)
        print("  ERROR: No API Key found (OPENROUTER, GEMINI, or GROQ)!")
        print("  Please check your .env file.")
        print("=" * 60)
        sys.exit(1)

    pause_event = threading.Event()
    context = {"pause_event": pause_event}

    from core.registry import SkillRegistry
    registry = SkillRegistry()
    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    registry.load_skills(skills_dir, context=context)
    
    if args.text:
        print("\n" + "=" * 50)
        print("  LUMI AI ASSISTANT - TEXT MODE")
        print("  Type commands to interact. Type 'quit' to exit.")
        print("=" * 50 + "\n")
        lumi_loop(pause_event, registry, args)
    else:
        t = threading.Thread(target=lumi_loop, args=(pause_event, registry, args), daemon=True)
        t.start()
        
        try:
            from gui.wave_ui import run_gui as run_gui_app
            run_gui_app(pause_event)
        except Exception as e:
            print(f"\n[!] GUI ERROR: {e}")
            print("Running in VOICE ONLY mode (Terminal)...")
            # Wait for the voice thread (t) to finish since we are now in CLI mode
            t.join()

if __name__ == "__main__":
    main()