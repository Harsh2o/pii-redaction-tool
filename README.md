# PII Redaction Tool

![Python](https://img.shields.io/badge/Python-3.10-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Assignment%20Submission-success)

This project implements a hybrid PII redaction pipeline using Microsoft Presidio, custom regex recognizers, and document derived entity extraction. It is designed to accurately detect and redact Personally Identifiable Information (PII) from `.docx` files while preserving the original document formatting.

## Example Output

- Document size: 1006 paragraphs
- Processing time: 129s
- Peak memory: 84.6MB
- Total entities detected: 9264

### Before / After

```text
Before:
Sarthak Malvadkar
cs.connect@kshinternational.com

After:
Rahul Sharma
rahul.sharma@example.com
```

## Architecture

The tool uses a multi stage approach to ensure high recall without sacrificing formatting integrity:

```text
    Input DOCX
         │
         ▼
┌─────────────────────────────┐
│  Entity Detection           │
│  - Microsoft Presidio       │
│  - Custom Regex Models      │
│  - Document Derived Orgs    │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Conflict Resolution        │
│  - Overlap filtering        │
│  - Sub string exclusion     │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Faker Replacement          │
│  - en_IN locale caching     │
│  - Context aware generation │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Formatting Preservation    │
│  - Run level mapping        │
│  - Paragraph fallback build │
└──────────┬──────────────────┘
           │
           ▼
      Output DOCX
```

## Features

- **Hybrid Detection:** Uses `spaCy` (en_core_web_sm) alongside Presidio to detect standard entities (Names, Emails, Orgs, Locations), augmented by custom RegEx for Indian PII (CIN, PAN, Aadhaar, Phone Numbers).
- **Format Preserving:** Uses a safe two step replacement strategy to prevent document corruption. It prioritizes run level `str.replace` and falls back to a full paragraph rebuild only when an entity crosses styling boundaries.
- **Consistent Redaction:** Uses `Faker` with a caching mechanism to ensure the same real entity is always mapped to the same fake entity across the document.
- **Evaluation Pipeline:** Includes a built in testing script that calculates Precision, Recall, and F1 Score against a deterministic ground truth subset.

## Project Structure

```text
PII-Redaction-Tool/
├── tests/
├── redact.py
├── recognizers.py
├── anonymizers.py
├── evaluator.py
├── ground_truth.py
├── config.yaml
├── requirements.txt
└── README.md
```

## Quick Start

```bash
git clone https://github.com/Harsh2o/pii-redaction-tool.git
cd pii-redaction-tool
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Basic redaction
python redact.py --input "Red Herring Prospectus.docx" --output redacted_output.docx
```


## Usage
```bash
# Run with higher accuracy (uses en_core_web_lg model)
python redact.py --input "Red Herring Prospectus.docx" --output redacted_output.docx --high-accuracy

# Display processing statistics (--stats)
python redact.py --input "Red Herring Prospectus.docx" --output redacted_output.docx --stats

# Generate JSON summary report & evaluate against ground truth
python redact.py --input "Red Herring Prospectus.docx" --output redacted_output.docx --report summary_report.json --evaluate

# Run unit tests
python -m pytest tests/ -v
```

## Configuration

Settings are managed via `config.yaml`. You can toggle specific PII types on or off, adjust the confidence threshold, and explicitly whitelist organizations that should not be redacted (e.g., regulatory bodies like SEBI or RBI).

## Key Design Decisions

- **Date Redaction:** The tool intentionally does not redact general historical or corporate dates because the assignment specifies only Dates of Birth as PII. This improves precision and reduces false positives. Dates are only redacted when they appear near context keywords (`dob`, `date of birth`, `born on`, etc.).
- **High Recall Strategy:** The tool intentionally favors recall over precision because the assignment prioritizes recall. Some organization and person entities may be over detected in dense legal documents, which is a safer trade off for redaction workflows.
- **Confidence Threshold:** Set to `0.45` — lower than Presidio's default of `0.6`. This was tested to maximize recall (catching more PII) at a slight cost to precision, which is prioritized for redaction tasks.
- **Document Derived Entities:** The tool does a fast initial pass over the document to extract known organizations and names, converting them into a high-priority deny list for Presidio. This catches entities that standard NLP models frequently misclassify.
- **Evaluation Metrics:** The evaluation set is a deterministic subset of manually verified PII instances and does not represent corpus wide performance. Because the tool prioritizes recall, expect some benign entities to be redacted, but precision on the ground truth deterministic set remains 100%.

## Future Improvements

- OCR support
- PDF support
- Parallel processing
- Additional international recognizers
- A Web interface/dashboard for uploading documents and visually verifying detections before replacement.
