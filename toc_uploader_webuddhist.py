import requests

from utils import (
    get_token,
    read_json_file,
    fuzzy_match
)

class TableOfContentsUploader:
    def __init__(self, toc_upload_url: str = "https://api.webuddhist.com/api/v1/texts/table-of-content"):
        self.text_name = input("Enter the text name: ")
        self.payload_data_file_path = f"{self.text_name}/{self.text_name}_payload/{self.text_name}_root_text_toc_payload.json"
        self.payload_data = read_json_file(self.payload_data_file_path)
        self.toc_upload_url = toc_upload_url
        self.text_id_look_up_json_path = f"{self.text_name}/{self.text_name}_api_response/{self.text_name}_segment_content_with_segment_id.json"

    def upload_toc_to_webuddhist(self, data, token):
        response = requests.post(self.toc_upload_url, json=data, headers={"Authorization": f"Bearer {token}"})
        return response.json()

    def search_matching_content_index(self, content, look_up_list, last_found):
        for i in range(last_found, len(look_up_list)):
            if fuzzy_match(look_up_list[i]["segment_content"], content):
                return i
        raise ValueError(f"Content {content} not found in look_up_list")

    def replace_segment_content_with_id_in_toc(self, data, text_id_look_up_list):
        last_found = 0
        for section in data["sections"]:
            for segment in section["segments"]:
                found_index = self.search_matching_content_index(content = segment['segment_id'], look_up_list = text_id_look_up_list, last_found = last_found)
                segment['segment_id'] = text_id_look_up_list[found_index]["id"]
                last_found = found_index + 1
        return data

    def upload_toc(self):
        token = get_token()
        updated_toc_data = self.replace_segment_content_with_id_in_toc(self.payload_data, self.text_id_look_up_list)
        response = self.upload_toc_to_webuddhist(updated_toc_data, token)
        return response

if __name__ == "__main__":

    toc_uploader = TableOfContentsUploader()

    response = toc_uploader.upload_toc()

    print(response)

        
