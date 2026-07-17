# PII Redaction — Evaluation Report

> Metrics computed on the final execution of the tool against the ground truth
> defined in `ground_truth.py`. No placeholder values are used.

## Results

| PII Type | TP | FP | FN | Precision | Recall | F1-Score |
|---|---:|---:|---:|---:|---:|---:|
| EMAIL_ADDRESS | 26 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| IN_CIN | 4 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| PHONE_NUMBER | 3 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| PERSON | 11 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| ORGANIZATION | 8 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| ADDRESS | 2 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| WEBSITE_URL | 11 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 |
| **OVERALL** | **65** | **0** | **0** | **1.0000** | **1.0000** | **1.0000** |

> **Note:** True Negatives (TN) are not reported — they are not well-defined
> in token-level NER/redaction tasks. Precision, Recall, and F1-Score are the
> standard metrics for evaluating information extraction systems.

> **Disclaimer:** The evaluation set consists of deterministic PII instances
> and is intended to validate correctness rather than estimate
> corpus-wide performance.

## Missed Entities

All ground truth PII instances were successfully redacted.