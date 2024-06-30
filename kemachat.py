# this was written in about 8 minutes so the code is terribel fr

import requests
import datetime

import uuid
import json
import os

api = "https://sped.lol"
s = requests.session()

messages_already_printed = []
DISPLAY_NAME = input("Enter a display name: ")

def print_all():
    for m in messages_already_printed:
        print(f"[{m[1]}] {m[2]}")

def get_messages():
    msgs = s.get(api + "/get_messages").json()

    for msg in msgs:
        user_id = msg["user_id"]
        text: str = msg["text"]
        display_name = msg["user_id"]
        stamp = msg["stamp"]
        
        full_message = [stamp, display_name, text]
        if full_message not in messages_already_printed:
            messages_already_printed.append(full_message)

def send_message(content: str):
    if len(content) == 0:
        return
    
    stamp = datetime.datetime.now(datetime.UTC).strftime("%X")
    message = {
        "user_id": DISPLAY_NAME,
        "avatar": "",
        "text": content,
        "stamp": stamp,
    }

    s.post(api + "/send_message",  headers={"Content-Type": "application/json"}, data=json.dumps(message))

get_messages()
print_all()

while True:
    os.system("cls")
    print_all()
    send_message(input("\nType your message, leave empty if you just want to refresh the chat: "))
    get_messages()
