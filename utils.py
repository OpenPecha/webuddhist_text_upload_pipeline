import requests
import json
from typing import Any, Dict, Iterator, List, Optional
import hashlib

TOKEN_API_URL = "https://api.webuddhist.com/api/v1/auth/login"



def get_token():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    response = requests.post(TOKEN_API_URL, json={"email": email, "password": password})
    return response.json()["auth"]["access_token"]

def read_json_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def iter_segment_ids_from_toc_dict(toc: Dict[str, Any], text_id_look_up_dict: Dict[str, Any]) -> Iterator[str]:
    """Yield every segment_id from a TableOfContent-like dict.

    The expected shape matches:
    - toc: { "sections": [ Section, ... ] }
    - Section: {
        "segments": [{"segment_id": str, "segment_number": int}],
        "sections": [Section, ...] | None
      }
    """

    sections_stack: List[Dict[str, Any]] = list(toc.get("sections") or [])

    while sections_stack:
        section: Dict[str, Any] = sections_stack.pop()

        for segment in section.get("segments") or []:
            segment_id: Optional[str] = segment.get("segment_id")
            if segment_id:
                hash_content = hashlib.sha256(segment_id.encode("utf-8")).hexdigest()
                if hash_content in text_id_look_up_dict:
                    segment["segment_id"] = text_id_look_up_dict[hash_content]
                else:
                    raise ValueError(f"Segment content {segment_id} not found in text_id_look_up_dict")
                yield segment["segment_id"]

        child_sections = section.get("sections") or []
        if child_sections:
            sections_stack.extend(child_sections)


def print_segment_ids_from_toc(toc: Dict[str, Any], text_id_look_up_dict: Dict[str, Any]) -> None:
    """Print all segment_ids from an in-memory TOC dict as they are read."""

    for segment_id in iter_segment_ids_from_toc_dict(toc, text_id_look_up_dict):
        print(segment_id)

    return toc