import json
import os

JSON_FILE = 'config.json'

def load_user_data():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_user_data(data):
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
