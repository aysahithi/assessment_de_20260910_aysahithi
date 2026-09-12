

# NOTES

## Time Spent
- Approx. **9 hours total** spread across several days.  
- Majority of time on ingestion script and dbt models.  
- Additional effort on Airflow DAG setup and notebook walkthrough.

## Known Gaps
- Documentation is minimal (README only).  
- No extended polish or diagrams.  
- Pipeline tested locally but not hardened for production.  
- Stopped at **notebook stage**; no further docs or dashboards.

## AI Tool Usage
- Used AI tools for:
  - Git commands (reset, staging, force push).  
  - Structuring commit history into logical steps.  
  - Drafting README and NOTES skeletons.  
- Did **not** use AI to generate pipeline logic or code.  
- All ingestion, dbt, Airflow, and notebook logic written manually.

## Summary
- End‑to‑end pipeline runs successfully: **API → Postgres → dbt → Airflow → Notebook**.  
- Idempotent loads, schema tests, and notebook outputs demonstrate correctness.  
- Commit history shows incremental development.  
- Work completed up to notebook stage, as per assessment scope.

---

