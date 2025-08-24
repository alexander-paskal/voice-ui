import requests
import json
import base64

def query_gemini(api_key, conversation_history):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    headers = {"Content-Type": "application/json"}

    data = {"contents": conversation_history
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"


def add_text_message(history, role, text):
    history.append({
        "role": role,
        "parts": [{"text": text}]
    })

def add_image_message(history, role, image_path, text=""):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    parts = []

    if text:
        parts.append({"text": text})
    
    parts.append({
        "inline_data": {
            "mime_type": "image/png",
            "data": image_data

            }
        })

    history.append({
        "role": role, "parts": parts
        })



if __name__ == "__main__":
    import argparse
    import os
    import rich
    from rich.console import Console
    from rich.markdown import Markdown



    argparser = argparse.ArgumentParser()
    argparser.add_argument("--text", type=str, default="")
    argparser.add_argument("--image", type=str, default=None)
    args = argparser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("no api key found")
    history = []

    if args.image:
        add_image_message(history, "user", args.image, args.text)
    else:
        add_text_message(history, "user", args.text)
    

    text = query_gemini(api_key, history)

    console = Console()
    console.print(Markdown(text))

    
    
