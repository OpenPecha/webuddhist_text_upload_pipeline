from unittest import TestCase
from utils import (
    fuzzy_match,
    fuzzy_substring_match,
)


class TestUtils(TestCase):
    def test_fuzzy_match_identical_strings_returns_true(self):
        self.assertTrue(fuzzy_match("hello world", "hello world"))

    def test_fuzzy_match_different_strings_threshold_one_returns_false(self):
        self.assertFalse(fuzzy_match("hello world", "hello wo", threshold=0.95))

    def test_fuzzy_match_empty_strings_returns_true(self):
        self.assertTrue(fuzzy_match("", ""))

    def test_fuzzy_match_one_empty_returns_false(self):
        self.assertFalse(fuzzy_match("hello", ""))
        self.assertFalse(fuzzy_match("", "hello"))

    def test_fuzzy_substring_match_exact_substring_returns_true(self):
        self.assertTrue(fuzzy_substring_match("hello world", "Say hello world to everyone"))
    
    def test_fuzzy_substring_match_partial_different_strings_returns_true(self):
        self.assertTrue(fuzzy_substring_match("hello world to everyone", "Say hello world to everyones", threshold=0.95))

    def test_fuzzy_substring_match_not_present_returns_false(self):
        self.assertFalse(fuzzy_substring_match("goodbye", "Say hello world to everyone", threshold=0.95))

    def test_fuzzy_substring_match_empty_strings_returns_true(self):
        self.assertTrue(fuzzy_substring_match("", ""))

    def test_fuzzy_substring_match_one_empty_returns_false(self):
        self.assertFalse(fuzzy_substring_match("", "text"))
        self.assertFalse(fuzzy_substring_match("text", ""))
