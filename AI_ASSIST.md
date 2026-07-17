# AI Assistance Log

Document one place you used an LLM during this assignment.

## The problem

I needed to implement a payment type filter in my Streamlit dashboard that would update all dashboard panels (KPIs, hourly trend, and data freshness) using a single sidebar selection.

## The prompt

How can I implement a Streamlit sidebar filter for `payment_type_label` so that it updates all dashboard panels? I already have KPI queries, an hourly trip chart, and a data freshness panel that read from `fct_trips`. I want one `st.sidebar.selectbox` with an "All" option that applies the same SQL filter to every query while keeping `@st.cache_data`.

## The response

The LLM suggested creating a sidebar `selectbox`, building a reusable SQL `WHERE` clause based on the selected payment type, and inserting that clause into every query. It also suggested escaping single quotes in the selected value before building the SQL string.

## Reflection

I kept the overall approach of creating one reusable `where_clause` and applying it to every query. I also kept the handling of the "All" option. I reviewed the generated code, integrated it into my existing application, and verified that all dashboard panels updated correctly when the payment type changed.

---

> Remember: never paste real connection strings, passwords, or PII into an LLM.
> The NYC TLC dataset is public so sample rows are safe here, but practise the habit.
