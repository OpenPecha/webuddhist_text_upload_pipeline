import json
import os
import sys
import requests
from pathlib import Path
from unittest import TestCase
from unittest.mock import Mock, patch, mock_open

# Add the parent directory to the Python path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from segment_uploader_webuddhist import SegmentUploader
from utils import read_json_file


class TestSegmentUploader(TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.DATA_DIR = Path(__file__).parent / "data"
        self.test_text_name = "test_text"
        self.test_root_or_commentary = "root"
        self.payload_data_file_path = self.DATA_DIR / "dummy_segment_upload_payload.json"
        self.payload_data = read_json_file(str(self.payload_data_file_path))
        self.segment_upload_url = "https://api.webuddhist.com/api/v1/segments"
        self.segment_content_with_segment_id_file_path = self.DATA_DIR / "dummy_segment_content_with_segment_id.json"
        
        # Load expected API response
        self.expected_api_response = read_json_file(str(self.DATA_DIR / "dummy_api_response.json"))
        
        # Load expected segment content with segment id
        self.expected_segment_content_with_id = read_json_file(str(self.segment_content_with_segment_id_file_path))

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    def test_segment_uploader_initialization(self, mock_read_json, mock_input):
        """Test SegmentUploader initialization with mocked inputs."""
        # Mock user inputs
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        
        # Initialize SegmentUploader
        uploader = SegmentUploader()
        
        # Assertions
        self.assertEqual(uploader.text_name, self.test_text_name)
        self.assertEqual(uploader.root_or_commentary, self.test_root_or_commentary)
        self.assertEqual(uploader.payload_data, self.payload_data)
        expected_payload_path = f"{self.test_text_name}/{self.test_text_name}_payload/{self.test_text_name}_{self.test_root_or_commentary}_text_segment_payload.json"
        self.assertEqual(uploader.payload_data_file_path, expected_payload_path)

    @patch('segment_uploader_webuddhist.requests.post')
    def test_upload_segments_to_webuddhist_success(self, mock_post):
        """Test successful segment upload to webuddhist API."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = self.expected_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Create uploader instance with manual setup to avoid input prompts
        uploader = SegmentUploader.__new__(SegmentUploader)
        uploader.segment_upload_url = self.segment_upload_url
        
        # Test the upload method
        token = "test_token"
        result = uploader.upload_segments_to_webuddhist(self.payload_data, token)
        
        # Assertions
        mock_post.assert_called_once_with(
            self.segment_upload_url,
            json=self.payload_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(result, self.expected_api_response)

    @patch('segment_uploader_webuddhist.requests.post')
    def test_upload_segments_to_webuddhist_failure(self, mock_post):
        """Test failed segment upload to webuddhist API."""
        # Mock failed API response
        mock_response = Mock()
        mock_response.json.return_value = {"error": "Authentication failed"}
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        
        # Create uploader instance with manual setup
        uploader = SegmentUploader.__new__(SegmentUploader)
        uploader.segment_upload_url = self.segment_upload_url
        
        # Test the upload method
        token = "invalid_token"
        result = uploader.upload_segments_to_webuddhist(self.payload_data, token)
        
        # Assertions
        mock_post.assert_called_once()
        self.assertEqual(result, {"error": "Authentication failed"})

    @patch('builtins.open', new_callable=mock_open)
    @patch('segment_uploader_webuddhist.json.dump')
    def test_store_segment_content_with_segment_id_in_json(self, mock_json_dump, mock_file_open):
        """Test storing segment content with segment ID in JSON file."""
        # Create uploader instance with manual setup
        uploader = SegmentUploader.__new__(SegmentUploader)
        uploader.segment_content_with_segment_id_file_path = str(self.segment_content_with_segment_id_file_path)
        
        # Test the storage method
        uploader.store_segment_content_with_segment_id_in_json(self.expected_api_response)
        
        # Assertions
        mock_file_open.assert_called_once_with(str(self.segment_content_with_segment_id_file_path), "w", encoding="utf-8")
        mock_json_dump.assert_called_once()
        
        # Check the data structure passed to json.dump
        call_args = mock_json_dump.call_args
        dumped_data = call_args[0][0]  # First argument to json.dump
        
        # Verify the structure of dumped data
        self.assertEqual(len(dumped_data), len(self.expected_api_response["segments"]))
        for i, item in enumerate(dumped_data):
            self.assertIn("segment_content", item)
            self.assertIn("id", item)
            self.assertEqual(item["segment_content"], self.expected_api_response["segments"][i]["content"])
            self.assertEqual(item["id"], self.expected_api_response["segments"][i]["id"])

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    @patch('segment_uploader_webuddhist.get_token')
    @patch('segment_uploader_webuddhist.requests.post')
    @patch('builtins.open', new_callable=mock_open)
    @patch('segment_uploader_webuddhist.json.dump')
    def test_upload_segments_full_workflow(self, mock_json_dump, mock_file_open, 
                                         mock_post, mock_get_token, mock_read_json, mock_input):
        """Test the complete upload segments workflow."""
        # Setup mocks
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        mock_get_token.return_value = "test_token"
        
        mock_response = Mock()
        mock_response.json.return_value = self.expected_api_response
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        # Create and test uploader
        uploader = SegmentUploader()
        uploader.upload_segments()
        
        # Assertions
        mock_get_token.assert_called_once()
        mock_post.assert_called_once()
        mock_file_open.assert_called_once()
        mock_json_dump.assert_called_once()

    def test_payload_data_structure(self):
        """Test that the payload data has the expected structure."""
        self.assertIn("text_id", self.payload_data)
        self.assertIn("segments", self.payload_data)
        self.assertIsInstance(self.payload_data["segments"], list)
        
        # Test segment structure
        for segment in self.payload_data["segments"]:
            self.assertIn("content", segment)
            self.assertIn("type", segment)
            self.assertIn("mapping", segment)

    def test_api_response_structure(self):
        """Test that the expected API response has the correct structure."""
        self.assertIn("segments", self.expected_api_response)
        self.assertIn("text_id", self.expected_api_response)
        self.assertIn("status", self.expected_api_response)
        
        # Test segments structure in response
        for segment in self.expected_api_response["segments"]:
            self.assertIn("id", segment)
            self.assertIn("content", segment)
            self.assertIn("type", segment)
            self.assertIn("mapping", segment)

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    def test_custom_segment_upload_url(self, mock_read_json, mock_input):
        """Test SegmentUploader with custom upload URL."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        
        custom_url = "https://custom.api.com/segments"
        uploader = SegmentUploader(segment_upload_url=custom_url)
        
        self.assertEqual(uploader.segment_upload_url, custom_url)

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    @patch('segment_uploader_webuddhist.requests.post')
    def test_upload_with_empty_segments(self, mock_post, mock_read_json, mock_input):
        """Test upload behavior with empty segments list."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        
        empty_payload = {
            "text_id": "test_id",
            "segments": []
        }
        mock_read_json.return_value = empty_payload
        
        mock_response = Mock()
        mock_response.json.return_value = {"segments": [], "text_id": "test_id", "status": "success"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        uploader = SegmentUploader()
        result = uploader.upload_segments_to_webuddhist(empty_payload, "test_token")
        
        self.assertEqual(len(result["segments"]), 0)

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    @patch('segment_uploader_webuddhist.requests.post')
    def test_upload_segments_network_error(self, mock_post, mock_read_json, mock_input):
        """Test upload behavior when network error occurs."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        
        # Mock network error
        mock_post.side_effect = requests.exceptions.ConnectionError("Network error")
        
        uploader = SegmentUploader()
        
        # Test that the exception is raised
        with self.assertRaises(requests.exceptions.ConnectionError):
            uploader.upload_segments_to_webuddhist(self.payload_data, "test_token")

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    def test_file_not_found_error(self, mock_read_json, mock_input):
        """Test behavior when payload file is not found."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.side_effect = FileNotFoundError("File not found")
        
        # Test that the exception is raised during initialization
        with self.assertRaises(FileNotFoundError):
            SegmentUploader()

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    @patch('builtins.open')
    def test_file_write_permission_error(self, mock_open, mock_read_json, mock_input):
        """Test behavior when file write permission is denied."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        mock_open.side_effect = PermissionError("Permission denied")
        
        uploader = SegmentUploader()
        
        # Test that the exception is raised when trying to write file
        with self.assertRaises(PermissionError):
            uploader.store_segment_content_with_segment_id_in_json(self.expected_api_response)

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    @patch('segment_uploader_webuddhist.requests.post')
    def test_invalid_json_response(self, mock_post, mock_read_json, mock_input):
        """Test behavior when API returns invalid JSON."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        
        # Mock response with invalid JSON
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        
        uploader = SegmentUploader()
        
        # Test that the exception is raised
        with self.assertRaises(json.JSONDecodeError):
            uploader.upload_segments_to_webuddhist(self.payload_data, "test_token")

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    def test_malformed_payload_data(self, mock_read_json, mock_input):
        """Test behavior with malformed payload data."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        
        # Malformed payload missing required fields
        malformed_payload = {
            "segments": [
                {"content": "test", "type": "source"}  # Missing 'mapping' field
            ]
        }  # Missing 'text_id' field
        mock_read_json.return_value = malformed_payload
        
        uploader = SegmentUploader()
        
        # Test that the malformed data is still loaded (validation would be done by API)
        self.assertEqual(uploader.payload_data, malformed_payload)
        self.assertNotIn("text_id", uploader.payload_data)

    def test_segment_content_extraction_edge_cases(self):
        """Test segment content extraction with edge cases."""
        # Create uploader instance with manual setup
        uploader = SegmentUploader.__new__(SegmentUploader)
        uploader.segment_content_with_segment_id_file_path = "test_path.json"
        
        # Test with empty segments
        empty_response = {"segments": []}
        
        with patch('builtins.open', mock_open()) as mock_file:
            with patch('segment_uploader_webuddhist.json.dump') as mock_json_dump:
                uploader.store_segment_content_with_segment_id_in_json(empty_response)
                
                # Check that empty list is dumped
                call_args = mock_json_dump.call_args
                dumped_data = call_args[0][0]
                self.assertEqual(len(dumped_data), 0)

    @patch('segment_uploader_webuddhist.input')
    @patch('segment_uploader_webuddhist.read_json_file')
    @patch('segment_uploader_webuddhist.get_token')
    def test_token_retrieval_failure(self, mock_get_token, mock_read_json, mock_input):
        """Test behavior when token retrieval fails."""
        mock_input.side_effect = [self.test_text_name, self.test_root_or_commentary]
        mock_read_json.return_value = self.payload_data
        mock_get_token.side_effect = Exception("Token retrieval failed")
        
        uploader = SegmentUploader()
        
        # Test that the exception is raised during upload
        with self.assertRaises(Exception):
            uploader.upload_segments()

    def tearDown(self):
        """Clean up after each test method."""
        # Remove any temporary files that might have been created
        temp_files = [
            "temp.json",
            "test_output.json"
        ]
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)