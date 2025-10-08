import json
import requests
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Add src directory to Python path
src_dir = str(Path(__file__).resolve().parent.parent)
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Define base directory for file paths
BASE_DIR = Path(__file__).resolve().parent
MAPPING_DATA_DIR = BASE_DIR / "mapping_data"
LOOKUP_DIR = BASE_DIR / "lookup"
MAPPING_PAYLOAD_DIR = BASE_DIR / "mapping_payload"

from utils import (
    read_json_file,
    fuzzy_match,
    get_token
)

from mapping.mapping_models import (
    Mapping,
    TextMapping,
    ParentSegmentMapping
)

from typing import List

class CommentaryTextMapping:

    def __init__(self, mapping_upload_url: str = "https://api.webuddhist.com/api/v1/mappings"):
        self.mapping_upload_url = mapping_upload_url

        self.mapping_file_name = input("Enter the mapping file name: ")
        self.mapping_file_name_path = str(MAPPING_DATA_DIR / f"{self.mapping_file_name}.json")
        self.mapping_data = read_json_file(self.mapping_file_name_path)
        
        self.look_up_list_file_name_root = input("Enter the look up list file name for root: ")
        self.look_up_list_file_name_commentary = input("Enter the look up list file name for commentary: ")
        
        self.look_up_list_file_name_root_path = str(LOOKUP_DIR / "root" / f"{self.look_up_list_file_name_root}.json")
        self.look_up_list_file_name_commentary_path = str(LOOKUP_DIR / "commentary" / f"{self.look_up_list_file_name_commentary}.json")

        self.look_up_list_root = read_json_file(self.look_up_list_file_name_root_path)
        self.look_up_list_commentary = read_json_file(self.look_up_list_file_name_commentary_path)

        self.mapping_payload_file_path = str(MAPPING_PAYLOAD_DIR / f"{self.mapping_file_name}_mapping_payload.json")

    def validate_mapping_data_present_in_look_up_list(self):
        last_found_root = 0
        last_found_commentary = 0
        for mapping in self.mapping_data:
            root_found = False
            commentary_found = False
            if not mapping["root"] or len(mapping["root"]) == 0 or not mapping["commentary"] or len(mapping["commentary"]) == 0:
                continue
            
            for i in range(last_found_root, len(self.look_up_list_root)):
                if fuzzy_match(self.look_up_list_root[i]["segment_content"], mapping["root"]):
                    root_found = True
                    last_found_root = i + 1
                    break;

            for i in range(last_found_commentary, len(self.look_up_list_commentary)):
                if fuzzy_match(self.look_up_list_commentary[i]["segment_content"], mapping["commentary"]):
                    commentary_found = True
                    last_found_commentary = i + 1
                    break;

            if not root_found or not commentary_found:
                raise ValueError(f"Mapping data {mapping} not found in look up list")
            
        return True
            
    def replace_mapping_data_with_id(self):
        for mapping in self.mapping_data:
            
            if not mapping["root"] or len(mapping["root"]) == 0:
                continue

            for data in self.look_up_list_root:
                if fuzzy_match(data["segment_content"], mapping["root"]):
                    mapping["root"] = data["id"]
                    break

            # Replace commentary text with ID
            commentary_found = False
            for data in self.look_up_list_commentary:
                if fuzzy_match(data["segment_content"], mapping["commentary"]):
                    mapping["commentary"] = data["id"]
                    break

        return self.mapping_data

    def generate_mapping_payload(self):
        mapping_payload = []

        for mapping in self.mapping_data:
            if not mapping["root"] or len(mapping["root"]) == 0:
                continue

            mapping_payload.append(
                TextMapping(
                    text_id=self.text_id,
                    segment_id=mapping["commentary"],
                    mappings=[
                        ParentSegmentMapping(
                            parent_text_id=mapping["root"],
                            segments=[
                                mapping["root"]
                            ]
                        )
                    ]
                )
            )

        return Mapping(
            text_mappings=mapping_payload
        )

    def write_mapping_payload_to_file(self, mapping_payload):
        with open(self.mapping_payload_file_path, "w", encoding="utf-8") as file:
            json.dump(mapping_payload.model_dump(), file, ensure_ascii=False, indent=4)

    def upload_mapping_payload_to_webuddhist(self, mapping_payload):
        token = get_token()
        response = requests.post(self.mapping_upload_url, json=mapping_payload, headers={"Authorization": f"Bearer {token}"})
        return response.json()


    def map_text_and_upload_to_webuddhist(self):
        self.validate_mapping_data_present_in_look_up_list()
        
        self.replace_mapping_data_with_id()

        mapping_payload = self.generate_mapping_payload()

        self.write_mapping_payload_to_file(mapping_payload)

        self.upload_mapping_payload_to_webuddhist(mapping_payload)

if __name__ == "__main__":

    text_mapping = CommentaryTextMapping()

    text_mapping.map_text_and_upload_to_webuddhist()