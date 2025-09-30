import requests
import json
from typing import Any, Dict, Iterator, List, Optional
import hashlib
import unicodedata
import Levenshtein

TOKEN_API_URL = "https://api.webuddhist.com/api/v1/auth/login"

def get_token():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    response = requests.post(TOKEN_API_URL, json={"email": email, "password": password})
    return response.json()["auth"]["access_token"]

def read_json_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def temp_json_write(data):
    with open("temp.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


    # INSERT_YOUR_CODE
def fuzzy_match(a: str, b: str, threshold: float = 0.95) -> bool:
    """
    Returns True if the similarity ratio between a and b is greater than or equal to the threshold percentage.
    Uses a simple Levenshtein distance algorithm for similarity.
    """

    if not a and not b:
        return True
    if not a or not b:
        return False

    distance = Levenshtein.jaro_winkler(a, b)

    return distance >= threshold


    # INSERT_YOUR_CODE
def show_hidden_literals(text: str) -> str:
    """
    Returns a string where hidden/zero-width characters are replaced with their Unicode codepoint in brackets.
    Useful for visualizing invisible characters like zero-width space, joiner, etc.
    """
    # List of common zero-width and hidden characters
    hidden_chars = [
        '\u200B', # ZERO WIDTH SPACE
        '\u200C', # ZERO WIDTH NON-JOINER
        '\u200D', # ZERO WIDTH JOINER
        '\u2060', # WORD JOINER
        '\uFEFF', # ZERO WIDTH NO-BREAK SPACE
        '\u180E', # MONGOLIAN VOWEL SEPARATOR
        '\u202A', # LEFT-TO-RIGHT EMBEDDING
        '\u202B', # RIGHT-TO-LEFT EMBEDDING
        '\u202C', # POP DIRECTIONAL FORMATTING
        '\u202D', # LEFT-TO-RIGHT OVERRIDE
        '\u202E', # RIGHT-TO-LEFT OVERRIDE
    ]
    def replace_hidden(c):
        if c in hidden_chars:
            name = unicodedata.name(c, "UNKNOWN")
            return f"[U+{ord(c):04X} {name}]"
        return c
    return ''.join(replace_hidden(c) for c in text)

def print_hidden_literals(text: str):
    """
    Prints the text with hidden/zero-width characters made visible.
    """
    print(show_hidden_literals(text))



if __name__ == "__main__":
    print(fuzzy_match(" བམ་པོ་གཅིག་གོ །\n", "བམ་པོ་གཅིག་གོ །\n"))