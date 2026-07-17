"""
tests/test_recognizers.py

Unit tests for the custom PII recognizers.
Tests each recognizer with known positive and negative examples.

Run with:
    python -m pytest tests/ -v
or:
    python tests/test_recognizers.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from presidio_analyzer import AnalyzerEngine
from recognizers import build_recognizer_registry


def build_test_analyzer():
    """Build a lightweight analyzer with custom recognizers for testing."""
    from presidio_analyzer.nlp_engine import NlpEngineProvider
    nlp_cfg = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
    }
    provider = NlpEngineProvider(nlp_configuration=nlp_cfg)
    nlp_engine = provider.create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, default_score_threshold=0.4)
    for rec in build_recognizer_registry():
        analyzer.registry.add_recognizer(rec)
    return analyzer


def get_entity_types(analyzer, text: str) -> set:
    results = analyzer.analyze(text=text, language="en")
    return {r.entity_type for r in results}


def get_matched_texts(analyzer, text: str) -> list:
    results = analyzer.analyze(text=text, language="en")
    return [text[r.start:r.end] for r in results]


class TestCINRecognizer(unittest.TestCase):

    def setUp(self):
        self.analyzer = build_test_analyzer()

    def test_cin_detected(self):
        text = "CIN: U28129PN1979PLC141032"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertIn("IN_CIN", entity_types,
                      "CIN number should be detected")

    def test_cin_value_extracted(self):
        text = "Corporate Identity Number: U28129PN1979PLC141032"
        matched = get_matched_texts(self.analyzer, text)
        self.assertIn("U28129PN1979PLC141032", matched)

    def test_invalid_cin_not_flagged(self):
        # Random 10-digit number - should not match CIN pattern
        text = "Reference number: 1234567890"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertNotIn("IN_CIN", entity_types)


class TestEmailRecognizer(unittest.TestCase):

    def setUp(self):
        self.analyzer = build_test_analyzer()

    def test_standard_email(self):
        text = "Please email us at cs.connect@kshinternational.com"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertIn("EMAIL_ADDRESS", entity_types)

    def test_email_with_subdomains(self):
        text = "Contact: kshinternational.ipo@in.mpms.mufg.com"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertIn("EMAIL_ADDRESS", entity_types)


class TestIndianPhoneRecognizer(unittest.TestCase):

    def setUp(self):
        self.analyzer = build_test_analyzer()

    def test_mobile_number(self):
        text = "Call us at +91-9876543210"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertTrue(
            "IN_PHONE_NUMBER" in entity_types or "PHONE_NUMBER" in entity_types,
            "Mobile number should be detected"
        )

    def test_landline_number(self):
        """Landlines like +91 20 4505 3237 must be caught."""
        text = "Telephone: +91 20 4505 3237"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertTrue(
            "IN_PHONE_NUMBER" in entity_types or "PHONE_NUMBER" in entity_types,
            "Landline +91 20 4505 3237 should be detected"
        )

    def test_another_landline(self):
        text = "Tel: +91 22 40094400"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertTrue(
            "IN_PHONE_NUMBER" in entity_types or "PHONE_NUMBER" in entity_types,
            "Landline +91 22 40094400 should be detected"
        )


class TestPANRecognizer(unittest.TestCase):

    def setUp(self):
        self.analyzer = build_test_analyzer()

    def test_pan_with_context(self):
        text = "PAN number: ABCDE1234F"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertIn("IN_PAN", entity_types)


class TestDOBRecognizer(unittest.TestCase):

    def setUp(self):
        self.analyzer = build_test_analyzer()

    def test_dob_with_context_flagged(self):
        """Date near DOB keyword should be detected."""
        text = "Date of Birth: 15/08/1990"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertIn("DATE_OF_BIRTH", entity_types,
                      "DOB with context should be flagged")

    def test_corporate_date_not_flagged(self):
        """Corporate/IPO dates without DOB context should NOT be flagged as DOB."""
        text = "Dated December 10, 2025"
        entity_types = get_entity_types(self.analyzer, text)
        self.assertNotIn("DATE_OF_BIRTH", entity_types,
                         "Corporate date without DOB context should not be flagged as DATE_OF_BIRTH")


class TestOrgWhitelistLogic(unittest.TestCase):
    """
    Tests that public regulatory bodies are correctly identified.
    The whitelist filtering happens in redact.py, not the recognizer itself,
    so here we just verify SEBI is in the default whitelist config.
    """

    def test_sebi_in_whitelist(self):
        import yaml
        with open("config.yaml", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        whitelist = config.get("org_whitelist", [])
        self.assertIn("SEBI", whitelist, "SEBI must be in the org whitelist")

    def test_nse_in_whitelist(self):
        import yaml
        with open("config.yaml", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        whitelist = config.get("org_whitelist", [])
        self.assertIn("NSE", whitelist, "NSE must be in the org whitelist")


if __name__ == "__main__":
    unittest.main(verbosity=2)
