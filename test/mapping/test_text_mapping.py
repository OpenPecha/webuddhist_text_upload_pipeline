from src.mapping.text_mapping import CommentaryTextMapping
from unittest import TestCase
from unittest.mock import patch
import os
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import read_json_file


class TestCommentaryTextMapping(TestCase):
    def setUp(self):
        self.mapping_upload_url = "https://127.0.0.1:8000/api/v1/mappings"

        self.root_text_id = "root_text_id"
        self.commentary_text_id = "commentary_text_id"

        self.mapping_file_name = "dummy_root_commentary_mapping_data"
        self.mapping_file_name_path = str(Path(__file__).parent / "mapping_data" / f"{self.mapping_file_name}.json")
        self.mapping_data = read_json_file(self.mapping_file_name_path)

        self.commentary_number = "1"

        self.look_up_list_file_name_root = "dummy_root_lookup"
        self.look_up_list_file_name_commentary = "dummy_commentary_lookup"

        self.look_up_list_file_name_root_path = str(Path(__file__).parent / "lookup" / "root" / f"{self.look_up_list_file_name_root}.json")
        self.look_up_list_file_name_commentary_path = str(Path(__file__).parent / "lookup" / "commentary" / f"{self.look_up_list_file_name_commentary}.json")

        self.look_up_list_root = read_json_file(self.look_up_list_file_name_root_path)
        self.look_up_list_commentary = read_json_file(self.look_up_list_file_name_commentary_path)

        self.mapping_payload_file_path = str(Path(__file__).parent / "mapping_payload" / f"{self.mapping_file_name}_mapping_payload.json")

        self.expected_replaced_root_text_with_segment_id = read_json_file(str(Path(__file__).parent / "expected_data" / "expected_replaced_root_text_with_segment_id.json"))
        self.expected_mapping_payload = read_json_file(str(Path(__file__).parent / "expected_data" / "expected_mapping_payload.json"))
        self.expected_mapping_dict = read_json_file(str(Path(__file__).parent / "expected_data" / "expected_mapping_dict.json"))

    @patch('src.mapping.text_mapping.input')
    @patch('src.mapping.text_mapping.read_json_file')
    def test_commentary_text_mapping_initialization(self, mock_read_json, mock_input):

        mock_input.side_effect = [self.root_text_id, self.commentary_text_id, self.mapping_file_name, self.commentary_number, self.look_up_list_file_name_root, self.look_up_list_file_name_commentary]

        # Return mapping_data, lookup_root, lookup_commentary in the same order as used in __init__
        mock_read_json.side_effect = [
            self.mapping_data,
            self.look_up_list_root,
            self.look_up_list_commentary
        ]

        text_mapping = CommentaryTextMapping(mapping_upload_url=self.mapping_upload_url)

        self.assertEqual(text_mapping.mapping_upload_url, self.mapping_upload_url)
        self.assertEqual(text_mapping.mapping_data, self.mapping_data)
        self.assertEqual(text_mapping.look_up_list_root, self.look_up_list_root)
        self.assertEqual(text_mapping.look_up_list_commentary, self.look_up_list_commentary)
    

    def test_replace_mapping_root_display_text_with_segment_id(self):
        
        text_mapping = CommentaryTextMapping.__new__(CommentaryTextMapping)
        text_mapping.mapping_data = self.mapping_data
        text_mapping.look_up_list_root = self.look_up_list_root

        is_mapping_root_segment_present_in_root_lookup_list = text_mapping.validate_mapping_root_segment_present_in_root_lookup_list()

        replace_mapping_root_display_text_with_segment_id = text_mapping.replace_mapping_root_display_text_with_id()

        self.assertTrue(is_mapping_root_segment_present_in_root_lookup_list)
        self.assertTrue(replace_mapping_root_display_text_with_segment_id)
        self.assertEqual(text_mapping.mapping_data, self.expected_replaced_root_text_with_segment_id)

    def test_root_display_text_of_mapping_data_not_present_in_root_lookup_list(self):

        text_mapping = CommentaryTextMapping.__new__(CommentaryTextMapping)
        text_mapping.mapping_data = self.mapping_data
        text_mapping.look_up_list_root = self.look_up_list_root

        text_mapping.mapping_data[1]["root_display_text"] = "This segment is not present in the root lookup list"

        with self.assertRaisesRegex(ValueError, f"Root {text_mapping.mapping_data[1]['root_display_text']} not found in look up list\nMapping data: {text_mapping.mapping_data[1]}"):
            text_mapping.validate_mapping_root_segment_present_in_root_lookup_list()


