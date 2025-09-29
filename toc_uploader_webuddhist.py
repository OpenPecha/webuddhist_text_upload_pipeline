import json
import requests

from utils import (
    get_token,
    read_json_file,
    print_segment_ids_from_toc,
)

TOC_PAYLOAD_FILE_PATH = "heart_sutra/heart_sutra_payload/toc.json"

WEBUDDHIST_API_URL = "https://api.webuddhist.com/api/v1/texts/table-of-content"

TEXT_ID_LOOK_UP_JSON_PATH = "heart_sutra/heart_sutra_api_response/heart_sutra_segment_content_with_segment_id.json"

def replace_segment_content_with_id_in_toc(data, text_id_look_up_dict):
    for section in data["sections"]:
        for segment in section["segments"]:
            if segment["segment_id"] in text_id_look_up_dict:
                segment["segment_id"] = text_id_look_up_dict[segment["segment_id"]]
            else:
                raise ValueError(f"Segment content {segment['segment_id']} not found in text_id_look_up_dict")
    return data

def upload_toc_to_webuddhist(data, token):
    response = requests.post(WEBUDDHIST_API_URL, json=data, headers={"Authorization": f"Bearer {token}"})
    return response.json()

if __name__ == "__main__":

    token = get_token()

    data = read_json_file(TOC_PAYLOAD_FILE_PATH)

    text_id_look_up_dict = read_json_file(TEXT_ID_LOOK_UP_JSON_PATH)

    # Print each segment_id as it is encountered
    updated_toc = replace_segment_content_with_id_in_toc(data, text_id_look_up_dict)

    response = upload_toc_to_webuddhist(updated_toc, token)

    print(response)

        
