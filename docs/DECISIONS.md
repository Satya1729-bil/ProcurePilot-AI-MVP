# Product & Technical Decisions
1. Rules before LLM for invoice matching: numeric and identity comparisons should be deterministic and testable.
2. Human review: the app flags exceptions but does not approve payments.
3. Synthetic dataset: safe and reproducible for a portfolio.
4. Lexical retrieval first: transparent and works without an embedding provider; evaluate embeddings later.
5. Optional LLM: core validation works if the provider is unavailable.
6. Metric honesty: dashboard counts seeded records; business-impact claims require separate evaluation.
7. MVP excludes OCR, ERP connectors, production SSO and autonomous agent actions.
