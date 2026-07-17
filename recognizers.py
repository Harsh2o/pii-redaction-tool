"""
recognizers.py

Custom Presidio recognizers for Indian-specific PII that the
default Presidio setup doesn't cover out of the box.

Each recognizer is a PatternRecognizer with regex patterns and
context keywords that boost confidence when nearby text matches.
"""

from presidio_analyzer import Pattern, PatternRecognizer


# CIN regex

def get_cin_recognizer():
    pattern = Pattern(
        name="cin_pattern",
        regex=r"\b[LU][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}\b",
        score=0.95
    )
    return PatternRecognizer(
        supported_entity="IN_CIN",
        patterns=[pattern],
        context=["cin", "corporate identity number", "company registration", "mca", "identity number"]
    )


# PAN recognizer
def get_pan_recognizer():
    pattern = Pattern(
        name="pan_pattern",
        regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
        score=0.85
    )
    return PatternRecognizer(
        supported_entity="IN_PAN",
        patterns=[pattern],
        context=["pan", "permanent account", "income tax", "pan card", "pan number"]
    )


# match spaced or continuous aadhaar
def get_aadhaar_recognizer():
    patterns = [
        Pattern("aadhaar_spaced",  r"\b\d{4}\s\d{4}\s\d{4}\b",  score=0.90),
        Pattern("aadhaar_hyphen",  r"\b\d{4}-\d{4}-\d{4}\b",    score=0.90),
        Pattern("aadhaar_compact", r"\b[2-9]{1}[0-9]{11}\b",    score=0.50),  # lower - ambiguous
    ]
    return PatternRecognizer(
        supported_entity="IN_AADHAAR",
        patterns=patterns,
        context=["aadhaar", "aadhar", "uid", "uidai", "unique identification", "enrolment"]
    )


# Pattern for Indian GSTIN (Goods and Services Tax Identification Number)
def get_gstin_recognizer():
    pattern = Pattern(
        name="gstin_pattern",
        regex=r"\b\d{2}[A-Z]{5}\d{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b",
        score=0.95
    )
    return PatternRecognizer(
        supported_entity="IN_GSTIN",
        patterns=[pattern],
        context=["gstin", "gst", "goods and services", "tax invoice", "gst number"]
    )


# Pattern for Indian phone numbers (mobile + landline)
def get_indian_phone_recognizer():
    patterns = [
        # Mobile: +91 followed by 10-digit number starting 6-9
        Pattern("in_mobile", r"\b(?:\+91[\s\-]?)?[6-9]\d{9}\b", score=0.85),
        # Landline: +91 + STD code (2-4 digits) + local number
        Pattern("in_landline", r"\+91[\s\-]?\d{2,4}[\s\-]?\d{3,5}[\s\-]?\d{4}\b", score=0.85),
        # Generic flexible - only fires with context
        Pattern("in_generic", r"(?:\+91[\s\-]?)?(?:\d[\s\-]?){8,12}\d", score=0.40),
    ]
    return PatternRecognizer(
        supported_entity="IN_PHONE_NUMBER",
        patterns=patterns,
        context=["phone", "telephone", "tel", "mobile", "contact", "fax", "call", "helpline"]
    )


# Pattern for Dates of Birth
def get_dob_recognizer():
    patterns = [
        Pattern("dob_ddmmyyyy",
                r"\b(0?[1-9]|[12]\d|3[01])[\/\-\.](0?[1-9]|1[0-2])[\/\-\.](?:19|20)\d{2}\b",
                score=0.50),
        Pattern("dob_iso",
                r"\b(?:19|20)\d{2}\-(0?[1-9]|1[0-2])\-(0?[1-9]|[12]\d|3[01])\b",
                score=0.50),
        Pattern("dob_written",
                r"\b(?:0?[1-9]|[12]\d|3[01])\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|"
                r"Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|"
                r"Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(?:19|20)\d{2}\b",
                score=0.50),
    ]
    # Context REQUIRED - without these keywords score stays at 0.50 (below threshold)
    return PatternRecognizer(
        supported_entity="DATE_OF_BIRTH",
        patterns=patterns,
        context=["date of birth", "dob", "d.o.b", "born on", "birth date", "birthdate", "born", "age"]
    )


# Pattern for Indian IFSC code (bank branch identifier)
def get_ifsc_recognizer():
    pattern = Pattern(
        name="ifsc_pattern",
        regex=r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
        score=0.80
    )
    return PatternRecognizer(
        supported_entity="IN_IFSC",
        patterns=[pattern],
        context=["ifsc", "ifsc code", "bank", "branch", "micr", "neft", "rtgs", "imps"]
    )


# Pattern for Website URLs
def get_url_recognizer():
    pattern = Pattern(
        name="url_pattern",
        regex=r"\bwww\.[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})?\b",
        score=0.80
    )
    return PatternRecognizer(
        supported_entity="WEBSITE_URL",
        patterns=[pattern],
        context=["website", "web", "visit", "url", "portal", "site"]
    )

# Company / Organization Names
# Uses a deny list of known companies found in the document,
# plus a context pattern for common Indian company suffixes.
def get_company_recognizer():
    # Known private companies found in the document (non-whitelist entities)
    known_companies = [
        "KSH International Limited",
        "KSH International",
        "Nuvama Wealth Management Limited",
        "Nuvama Wealth Management",
        "Nuvama",
        "ICICI Securities Limited",
        "ICICI Securities",
        "Trilegal",
        "IndusInd Bank",
        "Bajaj Finance Limited",
        "Bajaj Finance",
        "Bajaj Finserv",
        "Kirtane & Pandit",
        "Federal Bank",
        "Exim Bank",
        "Export Import Bank",
        "MUFG Bank",
        "Citibank",
        "Citi",
        "HDFC Bank",
        "HDFC Bank Limited",
    ]
    return PatternRecognizer(
        supported_entity="ORGANIZATION",
        deny_list=known_companies,
        context=["bank", "limited", "ltd", "securities", "company",
                 "corporation", "associates", "partners", "consultants",
                 "financial", "capital", "investments", "management"]
    )



def build_recognizer_registry():
    """Builds and returns a list of all custom recognizers for the Presidio analyzer."""
    return [
        get_cin_recognizer(),
        get_pan_recognizer(),
        get_aadhaar_recognizer(),
        get_gstin_recognizer(),
        get_indian_phone_recognizer(),
        get_dob_recognizer(),
        get_ifsc_recognizer(),
        get_url_recognizer(),
        get_company_recognizer(),
    ]

