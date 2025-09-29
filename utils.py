import requests
import json
from typing import Any, Dict, Iterator, List, Optional
import hashlib
import unicodedata

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