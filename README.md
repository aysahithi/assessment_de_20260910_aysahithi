# Data Engineering Assessment

Build **one small, working, end-to-end data pipeline** and walk through it in a notebook.  
Scope is deliberately small: the goal is a pipeline that actually runs, is safe to re-run, and can be explained clearly.

## The task

Daily weather for the cities in `config/cities.yml`, from the free  
[Open-Meteo archive API](https://open-meteo.com/en/docs/historical-weather-api) (no key), for the last 30 days.

```
Open-Meteo API ──extract──▶ raw_weather (Postgres)
                             │
                             └──dbt──▶ stg_weather ──▶ mart_weather
                                                         (tests + docs)
Airflow DAG: extract → load → dbt run → dbt test   (daily, backfillable)
Notebook: runs every stage, shows the results, explains the choices
```

---

## 1. Extract & Load (Python)

- Implemented in `ingestion/extract_load.py`.  
- One run loads **one logical date**; helper supports backfill for date ranges.  
- Re-running the same date does **not duplicate rows** (idempotent load).  
- API fields are kept unmodified in the raw table.  
- HTTP call includes retries and timeouts.

---

## 2. Transform (dbt)

- `raw_weather` declared as a **source**.  
- Staging model `stg_weather` types and cleans raw rows.  
- Mart model `mart_weather` aggregates daily metrics per city.  
- Schema tests: `unique`, `not_null`, sensible ranges.  
- Column descriptions included.

---

## 3. Orchestrate (Airflow)

- DAG in `dags/weather_pipeline.py`.  
- Flow: `extract → load → dbt run → dbt test`.  
- Driven by **logical date** (`{{ ds }}` / `data_interval_start`) so backfills work.  
- Tasks are idempotent; retries and timeouts configured.

---

## 4. Walkthrough (Notebook)

- `notebooks/walkthrough.ipynb` runs each stage using the same pipeline code.  
- Shows row counts, sample rows, dbt run/test output.  
- Demonstrates re-run safety (load same date twice, counts unchanged).  
- Queries the mart and shows a business-friendly result.  
- Markdown cells explain design choices.
## Notebooks

- `notebooks/walkthrough.ipynb` → original development walkthrough with explanations and outputs.
- `notebooks/walkthrough.reproduced.ipynb` → generated automatically via `make reproduce` to validate reproducibility.

---
NOTE:`make reproduce` executes the walkthrough notebook headlessly and writes `notebooks/walkthrough.reproduced.ipynb` as proof of reproducibility.


## Notes

- Work completed up to **notebook stage**.  
- Documentation is minimal; no extended polish beyond this README.  
- AI tools were used for guidance on Git commands and structuring commits, not for generating pipeline logic.  

---

## Reproducibility

Clone and run:

```bash
cp .env.example .env
make up          # postgres, airflow, jupyter
make airflow-ui  # http://localhost:8080 (admin/admin)
make notebook    # http://localhost:8888
make dbt         # dbt run inside airflow container
make reproduce   # executes notebooks/walkthrough.ipynb headlessly
make down
```

---

