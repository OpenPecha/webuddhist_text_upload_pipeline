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

        self.root_text_id = input("Enter the root text id: ")
        self.commentary_text_id = input("Enter the commentary text id: ")

        self.mapping_file_name = input("Enter the mapping file name: ")
        self.mapping_file_name_path = str(MAPPING_DATA_DIR / f"{self.mapping_file_name}.json")
        self.mapping_data = read_json_file(self.mapping_file_name_path)

        self.commentary_number = input("Enter the commentary number: ")
        
        self.look_up_list_file_name_root = input("Enter the look up list file name for root: ")
        self.look_up_list_file_name_commentary = input("Enter the look up list file name for commentary: ")
        
        self.look_up_list_file_name_root_path = str(LOOKUP_DIR / "root" / f"{self.look_up_list_file_name_root}.json")
        self.look_up_list_file_name_commentary_path = str(LOOKUP_DIR / "commentary" / f"{self.look_up_list_file_name_commentary}.json")

        self.look_up_list_root = read_json_file(self.look_up_list_file_name_root_path)
        self.look_up_list_commentary = read_json_file(self.look_up_list_file_name_commentary_path)

        self.mapping_payload_file_path = str(MAPPING_PAYLOAD_DIR / f"{self.mapping_file_name}_mapping_payload.json")

    def validate_mapping_root_segment_present_in_root_lookup_list(self):
        last_found = 0

        for mapping in self.mapping_data:
            if not mapping["root_display_text"] or len(mapping["root_display_text"]) == 0:
                continue

            root_text_found = False
            for index in range(last_found, len(self.look_up_list_root)):
                if fuzzy_match(self.look_up_list_root[index]["segment_content"], mapping["root_display_text"]):
                    last_found = index + 1
                    root_text_found = True
                    break

            if not root_text_found:
                raise ValueError(f"Root {mapping['root_display_text']} not found in look up list\nMapping data: {mapping}")

        return True

    def validate_commentary_lookup_list_present_in_mapping_data(self):
        last_found = 0
        for commentary_text in self.look_up_list_commentary:
            if not commentary_text["segment_content"] or len(commentary_text["segment_content"]) == 0:
                continue

            commentary_text_found = False
            for index in range(last_found, len(self.mapping_data)):
                if commentary_text["segment_content"] in self.mapping_data[index][f"commentary_{self.commentary_number}"]:
                    commentary_text_found = True
                    last_found = index + 1
                    break;

            if not commentary_text_found:
                raise ValueError(f"Commentary {commentary_text['segment_content']} not found in mapping data\nMapping data: {self.mapping_data}")

        return True
                    
            
    def replace_mapping_root_display_text_with_id(self):
        last_found = 0

        for mapping in self.mapping_data:
            if not mapping["root_display_text"] or len(mapping["root_display_text"]) == 0:
                continue

            root_text_found = False
            for index in range(last_found, len(self.look_up_list_root)):
                if fuzzy_match(self.look_up_list_root[index]["segment_content"], mapping["root_display_text"]):
                    mapping["root_display_text"] = self.look_up_list_root[index]["id"]
                    last_found = index + 1
                    root_text_found = True
                    break

            if not root_text_found:
                raise ValueError(f"Root {mapping['root_display_text']} not found in look up list\nMapping data: {mapping}")

        return True

    def get_mapping_dict(self):
        mapping_dict = {}

        for commentary_text in self.look_up_list_commentary:
            if not commentary_text["segment_content"] or len(commentary_text["segment_content"]) == 0:
                continue
        
            commentary_text_found = False
            for index in range(0, len(self.mapping_data)):
                if commentary_text["segment_content"] in self.mapping_data[index][f"commentary_{self.commentary_number}"]:
                    if commentary_text["segment_content"] not in mapping_dict:
                        mapping_dict[commentary_text["segment_content"]] = []
                    mapping_dict[commentary_text["id"]].append(self.mapping_data[index]["root_display_text"])
                    commentary_text_found = True
                    break
            
            if not commentary_text_found:
                raise ValueError(f"Commentary {commentary_text['segment_content']} not found in mapping data\nMapping data: {self.mapping_data}")

        return mapping_dict


    def generate_mapping_payload(self):

        mapping_dict: dict[str, List[str]] = self.get_mapping_dict()

        mapping_payload = []

        for key, value in mapping_dict.items():


        
                    

    def write_mapping_payload_to_file(self, mapping_payload):
        with open(self.mapping_payload_file_path, "w", encoding="utf-8") as file:
            json.dump(mapping_payload.model_dump(), file, ensure_ascii=False, indent=4)

    def upload_mapping_payload_to_webuddhist(self, mapping_payload):
        token = get_token()
        response = requests.post(self.mapping_upload_url, json=mapping_payload, headers={"Authorization": f"Bearer {token}"})
        return response.json()


    def map_text_and_upload_to_webuddhist(self):
        self.validate_mapping_root_segment_present_in_root_lookup_list()
        self.validate_commentary_lookup_list_present_in_mapping_data()
        
        self.replace_mapping_root_display_text_with_id()

        mapping_payload = self.generate_mapping_payload()

        self.write_mapping_payload_to_file(mapping_payload)

        self.upload_mapping_payload_to_webuddhist(mapping_payload)

if __name__ == "__main__":

    text_mapping = CommentaryTextMapping()

    text_mapping.map_text_and_upload_to_webuddhist()