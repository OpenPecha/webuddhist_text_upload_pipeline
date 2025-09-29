from pathlib import Path
import requests
import json 
import logging

logging.basicConfig(
    filename="metadata_upload_log.txt",
    filemode="a",
    encoding="utf-8",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)




class MetadataUploader:
    def __init__(self, api_key: str, base_url: str = "https://api.webuddhist.com/api/v1/"):
        self.api_key = api_key
        self.base_url = base_url

    def create_group(self, group_type: str):
        payload = {
            "type": group_type
        }   
        response = requests.post(self.base_url + "/groups", json=payload, headers={"Authorization": f"Bearer {self.api_key}"})
        logger.info(f"Group created: {response.status_code} {response.text}")
        if response.status_code != 200 or response.status_code != 201:
            raise Exception(f"Failed to create group: {response.status_code} {response.text}")
        else:
            print(f"Group created: {response.json()}")
            group_id = response.json()["id"]
        return group_id

    def upload_metadata(self, metadata: dict):
        group_id = self.create_group(metadata["group_type"])
        payload = {
            "title": metadata["title"],
            "language": metadata["language"],
            "isPublished": False,
            "group_id": group_id,
            "published_by": metadata["published_by"],
            "type": metadata["text_type"],
            "categories": [
                metadata["category_id"]
            ],
            "views": 0
            }
        response = requests.post(self.base_url, json=payload, headers={"Authorization": f"Bearer {self.api_key}"})
        logger.info(f"Metadata uploaded: {response.status_code} {response.text}")
        if response.status_code != 200 or response.status_code != 201:
            raise Exception(f"Failed to upload metadata: {response.status_code} {response.text}")
        else:
            print(f"Metadata uploaded: {response.json()}")
            text_id = response.json()["id"]
        return text_id
    

def read_json_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    

if __name__ == "__main__":
    metadata = read_json_file("data/metadata.json")
    metadata_uploader = MetadataUploader(api_key="your_api_key")
    for metadata in metadata:
        metadata_uploader.upload_metadata(metadata)
        