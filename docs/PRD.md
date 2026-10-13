# ProcurePilot AI — Product Requirements Document
**Version:** 1.0 MVP | **Status:** Portfolio specification

## Problem hypothesis
Procurement information may be spread across supplier records, purchase orders, invoices and contracts. Users can spend time searching for facts and spotting mismatches. A unified workflow may make information retrieval and exception identification easier. This is a hypothesis to validate, not a proven outcome.

## Personas
- **Accounts Payable Analyst:** compares invoices with purchase orders and investigates mismatches.
- **Procurement Specialist:** searches supplier and contract information.
- **Portfolio evaluator:** assesses product rationale, correctness, usability and delivery quality.

## Goals
1. Browse a reproducible synthetic dataset.
2. Validate PO reference, supplier, currency and total with deterministic rules.
3. Create explainable exceptions and record review status changes.
4. Answer questions from retrieved evidence and return source references.
5. Report transparent metrics without implying production impact.

## Non-goals
No payment approvals, real ERP integration, real customer data, production SSO, OCR, autonomous supplier-risk scoring or legal/financial advice.

## Functional requirements
- FR1: Seed synthetic suppliers, POs, invoices and contracts.
- FR2: Browse/search suppliers and browse invoices.
- FR3: Compare invoice fields to the linked PO with deterministic rules.
- FR4: Return each mismatch with expected and observed values.
- FR5: Missing PO or incomplete comparison yields Needs review.
- FR6: Failed validation creates or updates an exception.
- FR7: Review status can be Open, Under review, Resolved or Escalated.
- FR8: Status changes create audit events.
- FR9: Retrieve evidence before answering a question.
- FR10: Return source identifiers for retrieved records.
- FR11: No relevant evidence yields a limitation, not a guess.
- FR12: Metrics are computed from database state and labeled synthetic.
- FR13: Validate API inputs and return clear errors.
- FR14: Secrets are environment variables, not committed files.
- FR15: Clearly state the app is not for real payment decisions.

## Acceptance criteria examples
1. INV-901 linked to PO-600 flags total mismatch and returns expected/observed values.
2. INV-902 linked to PO-700 flags currency mismatch.
3. INV-903 with an unresolved PO reference returns Needs review.
4. A question mentioning INV-901 can return that invoice as a retrieved source.
5. An unrelated question with no relevant source returns no-evidence.
6. Updating exception status records an audit event and does not authorize payment.

## Success metrics to measure
- Mismatch precision = true mismatches flagged / all mismatches flagged in a labeled test set.
- Mismatch recall = true mismatches flagged / all true mismatches in the labeled set.
- Q&A factual correctness = answers meeting a predefined rubric / questions scored.
- Citation correctness = citations supporting the answer / citations reviewed.
- Task completion = tasks completed / tasks attempted in a scripted usability test.
- Median exception review time measured in a repeatable usability protocol.

## Risks and mitigations
- Hallucination: retrieve evidence, cite sources, test unanswerable questions.
- Financial calculation error: deterministic rules, unit tests and human review.
- Prompt injection: retrieved text is untrusted; the model has no write tools.
- Data leakage: synthetic data only and no secrets in Git.
- Inflated claims: publish test-set size, method, actual results and limitations.

## Product decisions
- Rule-based validation works independently of LLM availability.
- Full invoice total must equal PO total in this MVP; partial invoices are out of scope.
- Review status is a workflow state, not a financial approval.
- First retrieval version uses transparent lexical matching; embeddings can be tested later.
