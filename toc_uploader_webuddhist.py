import json
import requests

from utils import (
    get_token,
    read_json_file,
    fuzzy_match
)


TEXT_NAME = "heart_sutra"

TOC_PAYLOAD_FILE_PATH = f"{TEXT_NAME}/heart_sutra_payload/{TEXT_NAME}_root_text_toc_payload.json"

WEBUDDHIST_API_URL = "https://api.webuddhist.com/api/v1/texts/table-of-content"

TEXT_ID_LOOK_UP_JSON_PATH = f"{TEXT_NAME}/heart_sutra_api_response/{TEXT_NAME}_segment_content_with_segment_id.json"

def search_matching_content_index(content, look_up_list, last_found):
    for i in range(last_found, len(look_up_list)):
        if fuzzy_match(look_up_list[i]["segment_content"], content):
            return i
    raise ValueError(f"Content {content} not found in look_up_list")

def replace_segment_content_with_id_in_toc(data, text_id_look_up_list):
    last_found = 0
    for section in data["sections"]:
        for segment in section["segments"]:
            found_index = search_matching_content_index(content = segment['segment_id'], look_up_list = text_id_look_up_list, last_found = last_found)
            segment['segment_id'] = text_id_look_up_list[found_index]["id"]
            last_found = found_index + 1
    return data

def upload_toc_to_webuddhist(data, token):
    response = requests.post(WEBUDDHIST_API_URL, json=data, headers={"Authorization": f"Bearer {token}"})
    return response.json()

if __name__ == "__main__":

    token = get_token()

    data = read_json_file(TOC_PAYLOAD_FILE_PATH)

    text_id_look_up_list = read_json_file(TEXT_ID_LOOK_UP_JSON_PATH)

    # Print each segment_id as it is encountered
    updated_toc = replace_segment_content_with_id_in_toc(data, text_id_look_up_list)

    response = upload_toc_to_webuddhist(updated_toc, token)

    print(response)

        
