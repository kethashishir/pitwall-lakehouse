# PitWall Lakehouse Screenshot Checklist

Use this checklist before sharing the project on LinkedIn, GitHub, or your resume.

The goal is to show evidence, not decoration.

## Recommended screenshots

### 1. README landing page

Capture the top of the GitHub README showing:

- project name
- one-sentence summary
- architecture flow
- tech stack

Why it matters:

This is the first impression for recruiters and interviewers.

### 2. Streamlit Quality Evidence

Run:

~~~bash
make demo-fixture
~~~

Capture the `Quality Evidence` section showing:

- quality report found
- passed status
- total dbt result count

Why it matters:

It proves the dashboard is backed by validation evidence.

### 3. Streamlit Audit Evidence

Capture the `Audit Evidence` section showing:

- source-to-silver row-count differences
- duplicate lap-time audit
- missing pit-stop duration audit

Why it matters:

This is one of the strongest parts of the project. It shows real data-engineering judgment.

### 4. Streamlit Gold Marts

Capture the `Gold Marts` section showing one analytics mart table.

Good choices:

- `mart_race_summary`
- `mart_driver_pace`
- `mart_pit_stop_efficiency`
- `mart_constructor_reliability`

Why it matters:

It shows the final trusted outputs.

### 5. GitHub Actions green CI

Capture the successful CI workflow run showing:

- fixture pipeline passed
- Dagster fixture orchestration passed
- artifact upload completed

Why it matters:

It proves the project runs outside your laptop.

### 6. CI quality artifact

Open the GitHub Actions artifact named:

~~~text
pitwall-quality-report
~~~

Capture the artifact listing or downloaded report files.

Why it matters:

It shows CI preserves quality evidence.

### 7. Dagster materialization

Run:

~~~bash
make dagster-materialize-fixture
~~~

Capture either:

- successful terminal materialization logs
- Dagster UI asset graph if you run `make dagster-dev`

Why it matters:

It proves orchestration is part of the project, not just listed in the README.

### 8. Docker fixture pipeline

Run:

~~~bash
make docker-build
make docker-check
make docker-fixture-pipeline
~~~

Capture the final successful Docker fixture pipeline output.

Why it matters:

It proves the project can run in a clean Linux container.

## Screenshot rules

Use clean screenshots.

Avoid:

- giant terminal dumps
- screenshots showing secrets
- screenshots with unrelated tabs
- screenshots where the important result is too small to read

Prefer:

- cropped browser windows
- readable font size
- one idea per screenshot
- evidence-focused captions

## Suggested LinkedIn carousel order

1. Project title and architecture
2. Data quality evidence
3. Audit evidence
4. Gold marts
5. CI passing
6. Docker reproducibility
7. What I learned

## Suggested GitHub image folder

If screenshots are later committed, use:

~~~text
docs/images/
~~~

Suggested filenames:

~~~text
readme_landing.png
streamlit_quality_evidence.png
streamlit_audit_evidence.png
streamlit_gold_marts.png
github_actions_ci.png
ci_quality_artifact.png
dagster_materialization.png
docker_fixture_pipeline.png
~~~

Do not commit large raw screenshots. Compress images before committing.
