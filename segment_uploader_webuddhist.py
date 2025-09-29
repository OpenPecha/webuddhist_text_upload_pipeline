import json
from types import SimpleNamespace
import requests

WEBUDDHIST_API_URL = "https://api.webuddhist.com/api/v1/segments"

FILE_PATH = "choejuk_payload/choejuk_root_text_segment_payload.json"

def upload_segments_to_webuddhist(data):
    response = requests.post(WEBUDDHIST_API_URL, json=data)
    return response.json()

if __name__ == "__main__":


    with open(FILE_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    response = upload_segments_to_webuddhist(data)

    print(response)
    