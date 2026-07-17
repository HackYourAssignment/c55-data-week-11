# Week 11 Assignment: Build Two Dashboards

HackYourFuture Data Track, Week 11. The full brief (scenario, all three tiers, and submission steps) lives in the curriculum: **Week 11 → Assignment** in the HackYourFuture learning platform. Read it first; this repo only gets you started.

## What you build

Two dashboards reading the same `fct_trips` / `fct_daily_borough_stats` marts from Week 10, on Azure PostgreSQL:

- A **Metabase** analytical dashboard: point-and-click Questions and a shared Dashboard.
- A **Streamlit** metrics app: a code-first page with KPI, trend, and freshness panels.

Both get documented in `metric_definitions.md` so nobody argues about what a number means.

## What this repo gives you

This repo is a **ready-to-run Streamlit project** for the code-first dashboard, plus a destination for your Metabase deliverables:

```text
.
├── README.md                       <- TODO: your Metabase dashboard link / screenshots go here
├── AI_ASSIST.md                     <- TODO: template, document one LLM session
├── metric_definitions.template.md   <- copy into week11-streamlit/ (see below)
├── week11-streamlit/                <- ready-to-run: project config wired up, KPI panel is a TODO stub
│   ├── app.py                       <- TODO: implement the headline KPIs panel
│   ├── pyproject.toml
│   ├── uv.lock
│   └── .env.example                 <- copy to .env, fill in your credentials
└── .hyf/                            <- autograder, do not edit
```

- **Metabase**: build it directly in the HYF-managed Metabase instance. There is nothing to scaffold here. **Save your dashboard into the shared "Week 11 Submissions" collection** (not your personal collection) so your teacher can see and grade it, then put its link (plus screenshots or a PDF export) in this `README.md`, under "My submission" below.
- **Streamlit**: `week11-streamlit/` is already wired up (same `run_query` caching pattern taught in "Building a Metrics Dashboard", Week 11 Chapter 5) with page setup done and the headline-KPIs panel stubbed as `raise NotImplementedError(...)`. Your job is the query and the three `.metric()` tiles, not the project scaffolding:

```bash
cd week11-streamlit
uv sync
cp .env.example .env   # fill in your credentials
uv run streamlit run app.py
```

Once your KPI panel runs, copy the template into place and fill it in:

```bash
cp metric_definitions.template.md week11-streamlit/metric_definitions.md
```

Fill in `week11-streamlit/metric_definitions.md`: a five-field definition (name, description, calculation, data source, refresh frequency) for **every Metabase Question and every Streamlit panel** you build.

## My submission

<!-- TODO: 1) Save your Metabase dashboard into the shared "Week 11 Submissions" collection.
     2) Paste its link below, plus screenshots or a PDF export in this repo.
     3) Paste your 5-minute presentation recording link (keep it PRIVATE). -->

- Metabase dashboard (in the **Week 11 Submissions** collection): TODO
https://metabase-hyf.politepebble-abd3ebc2.westeurope.azurecontainerapps.io/dashboard/42-nyc-taxi-analytics-baraah
- Screenshots / PDF export: TODO Metabase_dashboard_baraah.png 
- Presentation recording (private, hosted in the Azure `student-submissions` container): TODO

https://hyfstoragedev.blob.core.windows.net/student-submissions/week-11/Baraah.mp4?sp=r&st=2026-07-16T15:33:03Z&se=2026-07-22T23:48:03Z&skoid=8bfd6dc9-8735-4bc5-8362-05ebddd6526b&sktid=07a14c4e-d88c-42f7-83b3-13af7e57ff3d&skt=2026-07-16T15:33:03Z&ske=2026-07-22T23:48:03Z&sks=b&skv=2026-02-06&spr=https&sv=2026-02-06&sr=b&sig=GRcWIO6iheJqLzk0s8zeJNoQLaZaSRw%2FGOD9scBdsYQ%3D

> ⚠️ **Keep the recording private.** It shows your screen and voice. Never make it public and never commit the `.mp4` (git history is forever). Check the frame for passwords, `.env` contents, or connection strings before uploading.

Host the recording in Azure: upload the `.mp4` to the shared `student-submissions` blob container (teachers get read access, nothing is public) and put the read-only link in your PR. The container is shared, so name your file after yourself: `week-11/<your-name>.mp4` (e.g. `week-11/jane-doe.mp4`). See "Host the recording on Azure Blob Storage" in the Week 11 Assignment chapter for the `az` CLI and Portal steps.

To upload by hand, [open the `hyfstoragedev` Storage browser in the Azure Portal](https://portal.azure.com/#@07a14c4e-d88c-42f7-83b3-13af7e57ff3d/resource/subscriptions/1120c89d-2a5f-4a15-a582-2ea34f0bb5c3/resourceGroups/rg-hyf-data/providers/Microsoft.Storage/storageAccounts/hyfstoragedev/storagebrowser) (sign in with your HYF account), then go to **Blob containers → student-submissions → Upload**.

## Packaging your submission for review

Your pull request should review itself: a reviewer should be able to understand and check it without asking you anything. When you open the PR, GitHub loads a template (`.github/PULL_REQUEST_TEMPLATE.md`) into the description, fill in every section. Two things carry the most weight:

- **Reproducible run instructions.** The Streamlit steps above must work from a clean clone against the reviewer's *own* Postgres: `uv sync`, copy `.env.example` to `.env`, set their own `POSTGRES_URL` (with `?sslmode=require`) and `DB_SCHEMA`, then `uv run streamlit run app.py`. Name every prerequisite, including your own `fct_trips` mart from Week 10. If a step only works on your machine, it is not reproducible.
- **Proof for what a reviewer cannot run.** A reviewer cannot open your private `dev_<name>` schema or your Metabase Questions, so commit screenshots (or a PDF export) of your Metabase dashboard and your running Streamlit app. Screenshots are how you prove "it runs on my data."

See "Package your pull request for review" in the Week 11 Assignment chapter for the full rationale.

## Check your score locally

The autograder runs static checks (required files present, secrets hygiene, Streamlit code patterns, metric-definition coverage):

```bash
bash .hyf/test.sh
cat .hyf/score.json
```

Passing score: 60/100. This covers the **Required** tier only: it cannot verify your dashboards render real data (that needs a live Azure Postgres connection CI does not have), so a passing score is necessary but not sufficient. Your teacher reviews the actual dashboards and presentation for Required/Extra credit.

## Submitting

Follow the Submission section of the assignment chapter: branch `week11/your-name`, commit, push, open a PR, and note in the PR description whether you also completed any Extra items plus your Metabase dashboard link.
