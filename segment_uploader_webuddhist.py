import json
import requests
import logging

from config import config
from utils import (
    get_token,
    read_json_file
)

LOG_FILE = "segment_upload_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

class SegmentUploader:
    def __init__(self, segment_upload_url: str = None):
        self.text_name = input("Enter the text name: ")
        self.root_or_commentary = input("Enter the root or commentary_[1,2,3]: ")
        self.payload_data_file_path = f"{self.text_name}/{self.text_name}_payload/{self.text_name}_{self.root_or_commentary}_text_segment_payload.json"
        self.payload_data = read_json_file(self.payload_data_file_path)
        self.segment_upload_url = segment_upload_url or config.get_segments_url()
        self.segment_content_with_segment_id_file_path = f"{self.text_name}/{self.text_name}_api_response/{self.text_name}_{self.root_or_commentary}_segment_content_with_segment_id.json"

    def upload_segments_to_webuddhist(self, payload_data,token):
        logger.info("Uploading segments to webuddhist")
        response = requests.post(self.segment_upload_url, json=payload_data, headers={"Authorization": f"Bearer {token}"})
        logger.info("Segments uploaded, ", response.status_code)
        return response.json()

    def store_segment_content_with_segment_id_in_json(self, response_data):
        logger.info("Storing segment content with segment id in json")
        list_segment_content_with_segment_id = []
        for _ in response_data["segments"]:
            segment_content = _["content"]
            list_segment_content_with_segment_id.append({"segment_content": segment_content, "id": _["id"]})
        
        with open(self.segment_content_with_segment_id_file_path, "w", encoding="utf-8") as file:
            json.dump(list_segment_content_with_segment_id, file, ensure_ascii=False, indent=4)


        logger.info("Segment content with segment id and hash id with segment content stored in json")

    def upload_segments(self):
        token = get_token()
        response = self.upload_segments_to_webuddhist(self.payload_data, token)
        self.store_segment_content_with_segment_id_in_json(response)

        logger.info("Segments uploaded successfully for text_id: ", self.payload_data["text_id"])


if __name__ == "__main__":
    
    segment_uploader = SegmentUploader()

    segment_uploader.upload_segments()
    