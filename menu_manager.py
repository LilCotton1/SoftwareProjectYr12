import json
import os

MENU_FILE = "menu.json"


def load_menu():
    if not os.path.exists(MENU_FILE):
        return {}
    with open(MENU_FILE, "r") as file:
        return json.load(file)


def save_menu(menu):
    with open(MENU_FILE, "w") as file:
        json.dump(menu, file, indent=4)