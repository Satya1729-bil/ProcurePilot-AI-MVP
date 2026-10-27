# ProcurePilot AI

**Catch invoice problems before they get paid.**

ProcurePilot checks each supplier invoice against its purchase order and contract. If the PO reference, supplier, currency or total doesn't match, it sends the invoice to an exception queue where someone can review it, and every status change is logged. An AI assistant answers questions about invoices, suppliers and contracts and points to the records it used. It runs locally with one Docker command, on synthetic data.

> This is an independent portfolio project inspired by common Source-to-Pay workflows. It is not an official Zycus product. All data is synthetic. Do not use it for real payment decisions or confidential data.

## What is implemented
- FastAPI backend and PostgreSQL data model.
- Synthetic suppliers, purchase orders, invoices and contract data.
- Rule-based invoice validation: PO reference, supplier, currency and total.
- Exception queue with status updates and audit events.
- Procurement Q&A using lexical retrieval over the seeded corpus; optional OpenAI generation with citations, and an extractive fallback without a key.
- React + TypeScript dashboard, invoice validation, exception review, supplier directory and AI assistant.
- Pytest unit tests, Docker Compose and GitHub Actions workflow.

## Run from scratch
Prerequisites: Git and Docker Desktop. No LLM API key is required for the core app.

1. Clone this repository and open the folder in VS Code.
2. Copy `.env.example` to `.env` (PowerShell: `Copy-Item .env.example .env`). The local default password is for demo only.
3. In the project root, run:
   ```bash
   docker compose up --build
   ```
4. Wait for services, then open:
   - Frontend: http://localhost:5173
   - FastAPI docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health
5. Click **Validate** for INV-901, INV-902 and INV-903 to create sample exceptions. Visit Exceptions to review them. Use AI Assistant to query invoice, supplier or contract IDs.
6. Stop with `Ctrl+C`, or run `docker compose down`. To delete the local database volume and reset all data, run `docker compose down -v` (destructive).

## Optional LLM mode
Set `OPENAI_API_KEY` in `.env` and optionally change `OPENAI_MODEL`. Restart Docker Compose. The app attempts to generate a grounded answer using retrieved evidence; if the provider fails, it falls back to retrieved excerpts. Never commit `.env` or API keys.

## Run tests
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```
Unit tests cover core validation logic and retrieval behavior. For a fully tested release, run the tests in your environment and inspect the CI result; do not claim tests passed until you have run them.

## API
- `GET /health`
- `GET /api/dashboard`
- `GET /api/suppliers?q=BluePeak`
- `GET /api/invoices`
- `GET /api/exceptions`
- `POST /api/invoices/{invoice_id}/validate`
- `PATCH /api/exceptions/{exception_id}/status`
- `POST /api/ask` with `{"question":"What is the amount for invoice INV-901?"}`

## Product management portfolio
Read `docs/PRD.md`, `docs/USER_STORIES.md`, `docs/PRODUCT_METRICS.md`, `docs/COMPETITIVE_RESEARCH_TEMPLATE.md`, `docs/DEMO_SCRIPT.md`, and `docs/DECISIONS.md`. These documents describe hypotheses and target metrics—not achieved business impact.

## Limitations to explain in interviews
- Synthetic dataset; not connected to an ERP.
- Initial retrieval is lexical, not embedding-based vector search.
- Optional LLM answer generation can still be wrong; citations must be checked.
- The demo has no production authentication, SSO, tenant isolation, OCR or payment actions.
- Invoice total equality is a simplifying MVP rule; partial invoices and tax/freight rules require domain discovery.
