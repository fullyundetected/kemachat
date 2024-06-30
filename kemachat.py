# this was written in about 8 minutes so the code is terribel fr

import requests
import datetime

import uuid
import json
import os

id = str(uuid.uuid4())
api = "https://sped.lol"
s = requests.session()

messages_already_printed = []
DISPLAY_NAME = input("Enter a display name: ")

def is_letter_or_num(t: str):
    # i thought a function for this already existed but i guess not
    for char in t:
        if char not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ":
            return False
    return True

while not is_letter_or_num(DISPLAY_NAME):
    print("Display name must be asciinumeric (kdots restriction not me)")
    DISPLAY_NAME = input("Enter a display name: ")

def parse_km_message(message):
    try:
        ms = message[15:]
        display_name_length = 0
        if ms[0] == "0":
            display_name_length = int(ms[1])
        else:
            display_name_length = int(ms[0:2])
        ms = ms[2:]
        display_name = ms[0:display_name_length]
        ms = ms[display_name_length:]
        return [display_name, ms]
    except:
        return []

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

        if text.startswith("KEMACHATMESSAGE"):
            display_name, text = parse_km_message(text)
        
        full_message = [stamp, display_name, text]
        if full_message not in messages_already_printed:
            messages_already_printed.append(full_message)

def send_message(content: str):
    if len(content) == 0:
        return
    
    stamp = datetime.datetime.now(datetime.UTC).strftime("%X")
    message = {
        "user_id": id,
        "avatar": "",
        "text": "KEMACHATMESSAGE" + str(len(DISPLAY_NAME))[0:2].rjust(2, "0") + DISPLAY_NAME + content,
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
