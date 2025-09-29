import json
import requests

from utils import (
    get_token,
    read_json_file,
    print_segment_ids_from_toc,
)

TOC_PAYLOAD_FILE_PATH = "choejuk/choejuk_payload/choejuk_root_text_toc_payload.json"

WEBUDDHIST_API_URL = "https://api.webuddhist.com/api/v1/texts/table-of-content"

TEXT_ID_LOOK_UP_JSON_PATH = "choejuk/choejuk_api_response/choejuk_content_hash_with_segment_id.json"

def upload_toc_to_webuddhist(data, token):
    response = requests.post(WEBUDDHIST_API_URL, json=data, headers={"Authorization": f"Bearer {token}"})
    return response.json()

if __name__ == "__main__":

    token = get_token()

    data = read_json_file(TOC_PAYLOAD_FILE_PATH)

    text_id_look_up_dict = read_json_file(TEXT_ID_LOOK_UP_JSON_PATH)

    # Print each segment_id as it is encountered
    updated_toc = print_segment_ids_from_toc(data, text_id_look_up_dict)

    response = upload_toc_to_webuddhist(updated_toc, token)

    print(response)

        
