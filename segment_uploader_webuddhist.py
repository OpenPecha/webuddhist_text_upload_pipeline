import json
import requests
import hashlib
import logging
import unicodedata

from utils import (
    get_token,
    read_json_file,
    fuzzy_match
)

WEBUDDHIST_API_URL = "https://api.webuddhist.com/api/v1/segments"

TEXT_NAME = "heart_sutra"

SEGMENT_PAYLOAD_FILE_PATH = f"{TEXT_NAME}/heart_sutra_payload/{TEXT_NAME}_root_text_segment_payload.json"

SEGMENT_CONTENT_WITH_SEGMENT_ID_FILE_PATH = f"{TEXT_NAME}/heart_sutra_api_response/{TEXT_NAME}_segment_content_with_segment_id.json"

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
    list_segment_content_with_segment_id = []
    for _ in data["segments"]:
        segment_content = _["content"]
        list_segment_content_with_segment_id.append({"segment_content": segment_content, "id": _["id"]})
    
    with open(SEGMENT_CONTENT_WITH_SEGMENT_ID_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(list_segment_content_with_segment_id, file, ensure_ascii=False, indent=4)


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
    