import requests
import json
from typing import Any, Dict, Iterator, List, Optional
import hashlib
import unicodedata

TOKEN_API_URL = "https://api.webuddhist.com/api/v1/auth/login"



def _strip_invisible(value: str) -> str:
    """Remove zero-width/invisible code points and normalize before hashing.

    Keeps meaningful whitespace (spaces, tabs, newlines) intact.
    """
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFC", value)
    invisible = {
        "\u200B",  # ZERO WIDTH SPACE
        "\u200C",  # ZERO WIDTH NON-JOINER
        "\u200D",  # ZERO WIDTH JOINER
        "\u200E",  # LEFT-TO-RIGHT MARK
        "\u200F",  # RIGHT-TO-LEFT MARK
        "\u2060",  # WORD JOINER
        "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE (BOM)
    }
    for ch in invisible:
        normalized = normalized.replace(ch, "")
    return normalized

def get_token():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    response = requests.post(TOKEN_API_URL, json={"email": email, "password": password})
    return response.json()["auth"]["access_token"]

def read_json_file(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

def clean_zero_width(text: str) -> str:
    """
    Remove all zero-width and invisible Unicode characters from the input string.

    Args:
        text (str): The input string to clean.

    Returns:
        str: The cleaned string with zero-width characters removed.
    """
    if text is None:
        return ""
    zero_width_chars = [
        "\u200B",  # ZERO WIDTH SPACE
        "\u200C",  # ZERO WIDTH NON-JOINER
        "\u200D",  # ZERO WIDTH JOINER
        "\u200E",  # LEFT-TO-RIGHT MARK
        "\u200F",  # RIGHT-TO-LEFT MARK
        "\u202A",  # LEFT-TO-RIGHT EMBEDDING
        "\u202B",  # RIGHT-TO-LEFT EMBEDDING
        "\u202C",  # POP DIRECTIONAL FORMATTING
        "\u202D",  # LEFT-TO-RIGHT OVERRIDE
        "\u202E",  # RIGHT-TO-LEFT OVERRIDE
        "\u2060",  # WORD JOINER
        "\u2061",  # FUNCTION APPLICATION
        "\u2062",  # INVISIBLE TIMES
        "\u2063",  # INVISIBLE SEPARATOR
        "\u2064",  # INVISIBLE PLUS
        "\uFEFF",  # ZERO WIDTH NO-BREAK SPACE (BOM)
    ]
    for ch in zero_width_chars:
        text = text.replace(ch, "")
    return text



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
            segment_id = segment["segment_id"]
            if segment_id:
                if segment_id in text_id_look_up_dict:
                    segment["segment_id"] = text_id_look_up_dict[segment_id]
                else:
                    print(segment_id)
                    print("here -> ",_visible_literal(segment_id["segment_id"]))
                    print(_visible_literal("​དེ་ནས་སངས་རྒྱས་ཀྱི་མཐུས། ​ཚེ་དང་ལྡན་པ་ཤཱ་རིའི་བུས་བྱང་ཆུབ་སེམས་དཔའ་ཆེན་པོ་འཕགས་པ་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་ལ་འདི་སྐད་ཅེས་སྨྲས་སོ། །\n"))
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


# removed visible literal helper and debug prints per user request
def _visible_literal(value):
    """Return a representation with control/zero-width whitespace escaped visibly.

    Keeps normal characters (including Tibetan) intact, but shows special whitespace
    explicitly so nothing is missed when printing.
    """
    if value is None:
        return ""
    replacements = {
        "\n": r"\n",
        "\r": r"\r",
        "\t": r"\t",
        "\u00A0": r"\u00A0",  # non-breaking space
        "\u200B": r"\u200B",  # zero-width space
        "\u200C": r"\u200C",  # zero-width non-joiner
        "\u200D": r"\u200D",  # zero-width joiner
        "\u2060": r"\u2060",  # word joiner
        "\uFEFF": r"\uFEFF",  # zero width no-break space (BOM)
    }
    return "".join(replacements.get(ch, ch) for ch in value)