# AI Assistance Log

Document one place you used an LLM during this assignment.

## The problem

<!-- TODO: describe the specific problem you asked an LLM about.
     Example: "My Streamlit KPI panel kept re-querying Postgres on every
     sidebar interaction even though I wrapped run_query in @st.cache_data." -->

While building the Streamlit dashboard, my "Trips by Hour of Day" chart was not displaying correctly. I wanted to check whether my SQL query and the data format passed to st.line_chart() were correct.

## The prompt

<!-- TODO: paste the exact prompt you sent to the LLM. -->

I have this Streamlit code for a line chart. The query runs successfully, but I want to make sure the data is in the correct format for st.line_chart(). Is there anything I should change?

st.subheader("Trips by Hour of Day")

hour_query = f"""
SELECT
    EXTRACT(HOUR FROM pickup_datetime) AS pickup_hour,
    COUNT(*) AS trip_count
FROM {DB_SCHEMA}.fct_trips
{payment_filter}
GROUP BY pickup_hour
ORDER BY pickup_hour;
"""

hour_df = run_query(hour_query)

st.line_chart(hour_df)

## The response

<!-- TODO: summarise or paste what the LLM returned. -->

The LLM explained that st.line_chart() works best when the x-axis is used as the DataFrame index. It suggested converting pickup_hour to an integer and setting it as the index before creating the chart.

## Reflection

<!-- TODO: what did you change, keep, or discard after reviewing the LLM's answer?
     Be specific: "I kept the cache_data suggestion but changed ttl from 60 to 300
     to match the mart's once-a-day refresh cadence." -->

I kept the suggestion to convert pickup_hour to an integer and used it as the DataFrame index before calling st.line_chart(). After making these changes, the chart displayed correctly and the hours appeared in the correct order.

---

> Remember: never paste real connection strings, passwords, or PII into an LLM.
> The NYC TLC dataset is public so sample rows are safe here, but practise the habit.
