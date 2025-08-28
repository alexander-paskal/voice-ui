from prompt import PROMPT
from tools import use_tool
from query_gemini import query_gemini, add_image_message, add_text_message
from speech_to_text import listen_and_transcribe
from scripts import call_script
from screen_grab import capture_screen
import os
import json
import time
import argparse





if __name__ == "__main__":
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--text-mode", action="store_true", help="activates text input mode")
    arg_parser.add_argument("--print-only", action="store_true", help="only prints model outputs")
    args = arg_parser.parse_args()


    while True:

        if args.text_mode:
            text = input("Enter prompt: ")
        else:
            text = None
            while text is None:
                text = listen_and_transcribe(verbose=1, pause_threshold=2)
        
        
        if call_script(text):
            continue



        new_prompt = PROMPT + "\n\n" + f"User's query is: {text}"
        
        capture_screen("screenshot.png")

        history = []
        api_key = os.getenv("GEMINI_API_KEY")
        add_text_message(history, "user", new_prompt)
        while True:
            capture_screen("screenshot.png")
            print("<screenshot>")
            
            add_image_message(history, "user", "screenshot.png")
            response = query_gemini(api_key, history)
            print(response)
            add_text_message(history, "model", response)
            if "terminate" in response:
                break

            else:
                
                try:
                    obj = json.loads(response)
                except:
                    print("invalid json response")
                    add_text_message(history, "user", "invalid json response")
                
                if isinstance(obj, dict):
                    obj = [obj]
                elif not isinstance(obj, list):
                    print("invalid json response")
                    add_text_message(history, "user", "invalid json response")
                    continue

                for cmd in obj:
                    if cmd.get("toolArguments") is None:
                        cmd["toolArguments"] = {}
                    try:
                        print("using tool")
                        use_tool(**cmd) if not args.print_only else print(cmd)
                        time.sleep(0.2)
                        

                    except:
                        add_text_message(history, "user", "invalid command")
                        print("invalid command")
                        break
                    
                    time.sleep(0.2)
        print("Finished")
            


