import json
import requests
import hashlib
import logging

from utils import (
    get_token,
    read_json_file
)

WEBUDDHIST_API_URL = "https://api.webuddhist.com/api/v1/segments"

SEGMENT_PAYLOAD_FILE_PATH = "choejuk/choejuk_payload/choejuk_root_text_segment_payload.json"

SEGMENT_CONTENT_WITH_SEGMENT_ID_FILE_PATH = "choejuk/choejuk_api_response/choejuk_segment_content_with_segment_id.json"

HASH_ID_WITH_SEGMENT_CONTENT_FILE_PATH = "choejuk/choejuk_api_response/choejuk_hash_id_with_segment_content.json"

LOG_FILE = "segment_upload_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def upload_segments_to_webuddhist(data, token):
    logger.info("Uploading segments to webuddhist")
    response = requests.post(WEBUDDHIST_API_URL, json=data, headers={"Authorization": f"Bearer {token}"})
    logger.info("Segments uploaded, ", response.status_code)
    return response.json()

def store_segment_content_with_segment_id_in_json(data):
    logger.info("Storing segment content with segment id in json")
    dict_segment_content_with_segment_id = {}
    dict_hash_id_with_segment_content = {}
    for _ in data["segments"]:
        hash_content = hashlib.sha256(_["content"].encode("utf-8")).hexdigest()
        dict_segment_content_with_segment_id[hash_content] = _["id"]
        dict_hash_id_with_segment_content[hash_content] = _["content"]
    
    with open(SEGMENT_CONTENT_WITH_SEGMENT_ID_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(dict_segment_content_with_segment_id, file, ensure_ascii=False, indent=4)
    


    with open(HASH_ID_WITH_SEGMENT_CONTENT_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(dict_hash_id_with_segment_content, file, ensure_ascii=False, indent=4)

    logger.info("Segment content with segment id and hash id with segment content stored in json")



if __name__ == "__main__":

    logger.info("Starting upload process")

    token = get_token()

    logger.info("Token obtained")

    logger.info("Reading file")

    data = read_json_file(SEGMENT_PAYLOAD_FILE_PATH)

    logger.info("File read")
    
    response = upload_segments_to_webuddhist(data, token)

    store_segment_content_with_segment_id_in_json(response)
    