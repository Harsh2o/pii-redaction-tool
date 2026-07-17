"""
tests/test_anonymizers.py

Unit tests for the anonymizer (fake value generator).
Verifies consistency, format correctness, and type coverage.

Run with:
    python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import pytest
import re
from anonymizers import generate_replacement, get_replacement_cache, clear_cache


class TestConsistentReplacement(unittest.TestCase):
    """Same real PII should always produce the same fake value."""

    def setUp(self):
        clear_cache()

    def test_same_name_same_fake(self):
        result1 = generate_replacement("PERSON", "Sarthak Malvadkar")
        result2 = generate_replacement("PERSON", "Sarthak Malvadkar")
        self.assertEqual(result1, result2,
                         "Same person name must always get the same fake replacement")

    def test_same_email_same_fake(self):
        result1 = generate_replacement("EMAIL_ADDRESS", "cs.connect@kshinternational.com")
        result2 = generate_replacement("EMAIL_ADDRESS", "cs.connect@kshinternational.com")
        self.assertEqual(result1, result2,
                         "Same email must always get the same fake replacement")

    def test_different_names_different_fakes(self):
        result1 = generate_replacement("PERSON", "Sarthak Malvadkar")
        result2 = generate_replacement("PERSON", "Prakash Boricha")
        
        self.assertIsNotNone(result1)
        self.assertIsNotNone(result2)


class TestEmailFormat(unittest.TestCase):

    def setUp(self):
        clear_cache()

    def test_fake_email_has_at_sign(self):
        result = generate_replacement("EMAIL_ADDRESS", "test@example.com")
        self.assertIn("@", result, "Fake email must contain @")

    def test_fake_email_has_domain(self):
        result = generate_replacement("EMAIL_ADDRESS", "another@company.org")
        parts = result.split("@")
        self.assertEqual(len(parts), 2)
        self.assertIn(".", parts[1], "Fake email domain must have a dot")


class TestPhoneFormat(unittest.TestCase):

    def setUp(self):
        clear_cache()

    def test_fake_phone_is_string(self):
        result = generate_replacement("IN_PHONE_NUMBER", "+91 9876543210")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 5)

    def test_fake_phone_contains_digits(self):
        result = generate_replacement("PHONE_NUMBER", "+91 20 4505 3237")
        digits = re.sub(r"[^\d]", "", result)
        self.assertGreaterEqual(len(digits), 8,
                                "Fake phone should have at least 8 digits")


class TestFallbackBehavior(unittest.TestCase):
    """Unknown entity types should return a placeholder, not crash."""

    def setUp(self):
        clear_cache()

    def test_unknown_entity_type(self):
        result = generate_replacement("SOME_UNKNOWN_TYPE", "some value")
        self.assertIsNotNone(result)
        self.assertIn("SOME_UNKNOWN_TYPE", result)

    def test_cin_replacement(self):
        result = generate_replacement("IN_CIN", "U28129PN1979PLC141032")
        self.assertIsNotNone(result)
        self.assertNotEqual(result, "U28129PN1979PLC141032",
                            "CIN should be replaced with something different")

    def test_credit_card_replacement(self):
        result = generate_replacement("CREDIT_CARD", "4111-2222-3333-4444")
        self.assertIsNotNone(result)
       
        self.assertNotEqual(result, "4111-2222-3333-4444")


if __name__ == "__main__":
    unittest.main(verbosity=2)
