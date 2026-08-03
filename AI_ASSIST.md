# AI Assistance Log

Document one place you used an LLM during this assignment.

## The problem

<!-- TODO: describe the specific problem you asked an LLM about.
     Example: "My Streamlit KPI panel kept re-querying Postgres on every
     sidebar interaction even though I wrapped run_query in @st.cache_data." -->
While working on the Week 11 Streamlit dashboard, I got a PostgreSQL error when the app tried to query `dev_halyna.fct_trips`.

The error was:

`relation "dev_halyna.fct_trips" does not exist`

At first I thought the problem was in my `SELECT` statement, but I was not sure whether the issue came from the SQL query, the database schema, or the Streamlit `.env` configuration.

## The prompt

<!-- TODO: paste the exact prompt you sent to the LLM. -->

I asked the LLM:

> My Streamlit app connects to Azure Postgres, but when it runs a query on `dev_halyna.fct_trips`, I get this error: `relation "dev_halyna.fct_trips" does not exist`. Is this a problem with the SELECT query, the schema, or the table? Please explain it simply.

## The response

<!-- TODO: summarise or paste what the LLM returned. -->

The LLM explained that the SQL aggregation itself was not the main problem. The error meant that PostgreSQL could not find the table `fct_trips` inside the schema `dev_halyna`.

It suggested checking whether the table exists in the database, whether the app is reading the correct `DB_SCHEMA` from the `.env` file, and whether the Week 10 mart table had been created in my own schema.

## Reflection

<!-- TODO: what did you change, keep, or discard after reviewing the LLM's answer?
     Be specific: "I kept the cache_data suggestion but changed ttl from 60 to 300
     to match the mart's once-a-day refresh cadence." -->

After checking the response, I verified the database table and confirmed that the problem was related to the missing `fct_trips` table in my schema, not to the `COUNT`, `AVG`, or `GROUP BY` logic.

I used the explanation to debug the issue step by step. I kept my Streamlit code close to the Week 11 material, using `run_query`, `@st.cache_data`, `st.metric`, `st.columns`, `st.line_chart`, and `st.sidebar.selectbox`.

I did not paste any real database password, full connection string, or private credentials into the LLM.

---

> Remember: never paste real connection strings, passwords, or PII into an LLM.
> The NYC TLC dataset is public so sample rows are safe here, but practise the habit.
