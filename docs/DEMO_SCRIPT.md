# 5-Minute Interview Demo

**0:00–0:30 — Problem:** Explain that this portfolio MVP uses synthetic data and is not a real payment system.

**0:30–1:15 — Dashboard:** Explain metrics are computed from the database and limited to seeded demo records.

**1:15–2:15 — Invoice validation:** Validate INV-901 (total mismatch), INV-902 (currency mismatch), and INV-903 (missing PO). Explain expected vs observed values.

**2:15–3:00 — Exception workflow:** Update a status and explain audit history. Status is not payment approval.

**3:00–4:00 — AI assistant:** Ask about INV-901, show retrieved source IDs, then ask an unrelated question and show the no-evidence behavior.

**4:00–5:00 — Product thinking:** Present the PRD, user story, acceptance criteria, metric plan, and trade-off: deterministic financial checks plus evidence-backed Q&A rather than autonomous financial actions.

## Interview questions to prepare
- Why this problem and persona?
- How did you prioritize the MVP?
- What evidence would validate product value?
- How would you reduce hallucinations?
- Why use rules for invoice comparison?
- What would you test with real users next?
