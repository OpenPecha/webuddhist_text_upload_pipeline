import json
import requests
from unittest import TestCase
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from toc_uploader_webuddhist import (
    TableOfContentsUploader
)
from utils import (
    read_json_file
)

class TestTableOfContentUploader(TestCase):
    def setUp(self):
        self.DATA_DIR = Path(__file__).parent / "data"
        self.test_text_name = "test_text"
        self.test_root_or_commentary = "root"
        self.payload_data_file_path = str(self.DATA_DIR / "dummy_toc_payload.json")
        self.payload_data = read_json_file(self.payload_data_file_path)
        self.toc_upload_url = "https://api.example.com/api/vi/table-of-content"
        self.text_id_look_up_json_path = str(self.DATA_DIR / "dummy_segment_content_with_segment_id.json")
        self.text_id_look_up_list = read_json_file(self.text_id_look_up_json_path)

        self.expected_toc_payload = read_json_file(str(self.DATA_DIR / "expected_dummy_toc_payload.json"))

    @patch('toc_uploader_webuddhist.input')
    @patch('toc_uploader_webuddhist.read_json_file')
    def test_toc_uploader_initialization(self, mock_read_json, mock_input):
        """Test TableOfContentsUploader initialization with mocked inputs."""
        # Mock user inputs
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        # Mock read_json_file to return payload data first, then lookup list
        mock_read_json.side_effect = [self.payload_data, self.text_id_look_up_list]

        uploader = TableOfContentsUploader()

        # Assertions
        self.assertEqual(uploader.text_name, self.test_text_name)
        self.assertEqual(uploader.root_or_commentary, self.test_root_or_commentary)
        self.assertEqual(uploader.payload_data, self.payload_data)
        self.assertEqual(uploader.text_id_look_up_list, self.text_id_look_up_list)
        
        # Check that the file paths match the expected format (absolute paths with src/data)
        expected_payload_path = str(
            (Path(__file__).parent.parent
             / "src"
             / "data"
             / self.test_text_name
             / f"{self.test_text_name}_payload"
             / f"{self.test_text_name}_{self.test_root_or_commentary}_text_toc_payload.json")
        )
        self.assertEqual(uploader.payload_data_file_path, expected_payload_path)

    def test_replace_segment_content_with_id_in_toc(self):

        uploader = TableOfContentsUploader.__new__(TableOfContentsUploader)
        
        replaced_payload_data = uploader.replace_segment_content_with_id_in_toc(self.payload_data, self.text_id_look_up_list)

        self.assertEqual(replaced_payload_data, self.expected_toc_payload)

        
    @patch('toc_uploader_webuddhist.requests.post')
    def test_upload_toc_to_webuddhist_success(self, mock_post):

        mock_response = Mock()
        mock_response.json.return_value = self.expected_toc_payload
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        uploader = TableOfContentsUploader.__new__(TableOfContentsUploader)
        uploader.toc_upload_url = self.toc_upload_url

        token = "test_token"
        result = uploader.upload_toc_to_webuddhist(self.payload_data, token)

        self.assertEqual(result, self.expected_toc_payload)

        mock_post.assert_called_once_with(self.toc_upload_url, json=self.payload_data, headers={"Authorization": f"Bearer {token}"})