# MVP User Stories & Acceptance Criteria

## PP-01 — Seed synthetic data
**Story:** As an evaluator, I want stable synthetic records so I can reproduce the demo.
- Seed suppliers, POs, invoices and contracts with stable IDs.
- Re-running startup does not duplicate seeded IDs.
- README discloses synthetic data.

## PP-02 — Browse supplier and invoice records
**Story:** As a procurement specialist, I want to find records so I can investigate issues.
- Supplier search matches name or ID.
- Invoice list shows invoice ID, supplier, PO, currency, amount and date.
- Empty/error states are understandable.

## PP-03 — Validate invoice against PO
**Story:** As an AP analyst, I want invoice data compared with its PO so I can identify discrepancies before review.
- Matching invoice returns No discrepancy found.
- Supplier, currency, total and missing-PO mismatches are individually reported.
- Each discrepancy includes field, expected value, observed value and rule.
- Validation never approves payment.

## PP-04 — Review exceptions
**Story:** As an AP analyst, I want failed validations to create reviewable exceptions.
- Failed validation creates or updates an exception.
- Reason is tied to an invoice and is readable.
- Status supports Open, Under review, Resolved and Escalated.
- Status updates create audit events.

## PP-05 — Ask procurement questions
**Story:** As a procurement specialist, I want to ask questions about records.
- Relevant records are retrieved before answer generation.
- Response returns source IDs.
- No relevant records yields insufficient evidence.
- LLM/provider failure does not break invoice validation.

## PP-06 — View metrics
**Story:** As an evaluator, I want transparent product metrics.
- Dashboard reports invoices, exceptions, open exceptions and resolved exceptions.
- Synthetic data is clearly labeled.
- Metrics are computed from database state, not hard-coded.

## PP-07 — Reproducible quality checks
**Story:** As a maintainer, I want automated tests and CI.
- Pytest runs on a clean checkout.
- Frontend TypeScript build runs in CI.
- A failing check fails the workflow.
- No API key is committed.
