from prompt import PROMPT
from tools import use_tool
from query_gemini import query_gemini, add_image_message, add_text_message
from scripts import call_script
from screen_grab import capture_screen
from plugins import execute_plugins
import yaml
import os
import json
import time
import argparse





if __name__ == "__main__":
    
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--text-mode", action="store_true", help="activates text input mode")
    arg_parser.add_argument("--print-only", action="store_true", help="only prints model outputs")
    arg_parser.add_argument("--plugins", default="plugins.yaml", help="Path to custom plugins")

    args = arg_parser.parse_args()
    with open(args.plugins) as f:
        plugins = yaml.safe_load(f)

    if not args.text_mode:
        from speech_to_text import listen_and_transcribe


    print("""
Hello! Welcome to voice-ui!
""")

    while True:

        if args.text_mode:
            text = input("Enter prompt: ")
        else:
            text = None
            while text is None:
                text = listen_and_transcribe(verbose=1, pause_threshold=1)
    

        if execute_plugins(text, plugins):
            continue

        if call_script(text):
            continue

        if call_script("press " + text):
            continue
        
        print("Unable to execute command")
    print("Finished")
            


