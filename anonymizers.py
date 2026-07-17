"""
anonymizers.py

Handles generating fake replacement values for detected PII.

Key design decision: consistent replacements.
If "Sarthak Malvadkar" appears 10 times in the doc,
it always maps to the same fake name - makes the redacted
document coherent and readable.

Uses Faker with en_IN locale for realistic Indian fake data.
"""

from faker import Faker
import random
import re

fake = Faker("en_IN")
# deterministic replacements for reproducibility
Faker.seed(42)

_REPLACEMENT_CACHE = {}


def _get_or_create(key: str, generator_fn):
    """Return cached fake value, or generate and cache a new one."""
    if key not in _REPLACEMENT_CACHE:
        _REPLACEMENT_CACHE[key] = generator_fn()
    return _REPLACEMENT_CACHE[key]


# Functions to generate specific types of fake data
def fake_person_name(original: str) -> str:
    return _get_or_create(original, fake.name)


def fake_email(original: str) -> str:
    def _gen():
        name = fake.first_name().lower() + "." + fake.last_name().lower()
        domain = random.choice(["example.com", "sample.in", "testmail.com", "demo.org"])
        return f"{name}@{domain}"
    return _get_or_create(original, _gen)


def fake_phone(original: str) -> str:
    def _gen():
        part1 = random.randint(60000, 99999)
        part2 = random.randint(10000, 99999)
        return f"+91 {part1} {part2}"
    return _get_or_create(original, _gen)


def fake_company(original: str) -> str:
    def _gen():
        return fake.company()
    return _get_or_create(original, _gen)


def fake_address(original: str) -> str:
    def _gen():
        return fake.address().replace("\n", ", ")
    return _get_or_create(original, _gen)


def fake_location(original: str) -> str:
    return _get_or_create(original, fake.city)


def fake_cin(original: str) -> str:
    def _gen():
        prefix = random.choice(["U", "L"])
        digits1 = str(random.randint(10000, 99999))
        state = random.choice(["MH", "DL", "KA", "TN", "GJ", "RJ", "UP", "WB"])
        year = str(random.randint(1960, 2020))
        company_type = random.choice(["PLC", "PTC", "FLC"])
        digits2 = str(random.randint(100000, 999999))
        return f"{prefix}{digits1}{state}{year}{company_type}{digits2}"
    return _get_or_create(original, _gen)


def fake_pan(original: str) -> str:
    def _gen():
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        part1 = "".join(random.choices(letters, k=5))
        part2 = str(random.randint(1000, 9999))
        part3 = random.choice(letters)
        return f"{part1}{part2}{part3}"
    return _get_or_create(original, _gen)


def fake_aadhaar(original: str) -> str:
    def _gen():
        first = str(random.randint(2, 9))
        rest = "".join([str(random.randint(0, 9)) for _ in range(11)])
        num = first + rest
        return f"{num[:4]} {num[4:8]} {num[8:]}"
    return _get_or_create(original, _gen)


def fake_gstin(original: str) -> str:
    return "[GSTIN_REDACTED]"


def fake_ip(original: str) -> str:
    return _get_or_create(original, fake.ipv4_private)


def fake_dob(original: str) -> str:
    def _gen():
        dob = fake.date_of_birth(minimum_age=25, maximum_age=70)
        return dob.strftime("%d/%m/%Y")
    return _get_or_create(original, _gen)


def fake_credit_card(original: str) -> str:
    return "4111-1111-1111-1111"


def fake_url(original: str) -> str:
    def _gen():
        name = fake.domain_word()
        return f"www.{name}.com"
    return _get_or_create(original, _gen)


def fake_ifsc(original: str) -> str:
    def _gen():
        banks = ["HDFC", "ICIC", "SBIN", "UTIB", "PUNB", "CBIN"]
        bank = random.choice(banks)
        branch = str(random.randint(1000000, 9999999))
        return f"{bank}0{branch[:6]}"
    return _get_or_create(original, _gen)


# Registry of how to handle each entity type
_FAKE_GENERATORS = {
    "PERSON": fake_person_name,
    "EMAIL_ADDRESS": fake_email,
    "PHONE_NUMBER": fake_phone,
    "IN_PHONE_NUMBER": fake_phone,
    "ORGANIZATION": fake_company,
    "LOCATION": fake_address,
    "GPE": fake_address,
    "IN_CIN": fake_cin,
    "IN_PAN": fake_pan,
    "IN_AADHAAR": fake_aadhaar,
    "IN_GSTIN": fake_gstin,
    "IN_IFSC": fake_ifsc,
    "IP_ADDRESS": fake_ip,
    "DATE_OF_BIRTH": fake_dob,
    "CREDIT_CARD": fake_credit_card,
    "WEBSITE_URL": fake_url,
    "URL": fake_url,
}


def generate_replacement(entity_type: str, original_value: str) -> str:
    """
    Looks up the right generator for the entity type and returns a fake string.
    If it's an unknown type, just returns a placeholder.
    """
    generator = _FAKE_GENERATORS.get(entity_type)
    if generator:
        try:
            return generator(original_value)
        except Exception:
            return f"[{entity_type}]"
    
    # Fallback for unexpected entities
    return f"[{entity_type}]"


def get_replacement_cache() -> dict:
    """Returns the full mapping of real -> fake values (for dry-run display)."""
    return dict(_REPLACEMENT_CACHE)


def clear_cache():
    """Reset the replacement cache (useful for testing)."""
    _REPLACEMENT_CACHE.clear()
