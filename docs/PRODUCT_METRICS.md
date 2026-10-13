# Product Metrics & Evaluation Plan

## North-star candidate
Successful procurement task completion rate in a scripted usability test.

## Metrics
- Invoice mismatch precision and recall on a labeled test set.
- Q&A factual correctness and citation correctness.
- Task completion rate and median task time in a repeatable usability protocol.
- API p95 latency under a documented local setup.
- Operational counts: invoices, exceptions, open and resolved exceptions.

## Measurement method
1. Define expected validation outcomes for every invoice in a fixed labeled dataset.
2. Run validations and compare results with expected labels.
3. Prepare 10–20 answerable and unanswerable questions with expected facts and source IDs.
4. Score responses against a rubric; publish test-set size and scoring method.
5. Run scripted usability tasks if making usability observations; treat small samples as exploratory.
6. Report measured numbers only. Do not claim enterprise savings based on synthetic records.

Precision = TP / (TP + FP). Recall = TP / (TP + FN). Task completion = completed tasks / attempted tasks. Citation correctness = supported citations / citations reviewed.
