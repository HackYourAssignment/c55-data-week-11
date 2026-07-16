# AI Assistance Log

Document one place you used an LLM during this assignment.

## The problem

When I tried to start the Streamlit dashboard, it could not connect to Azure PostgreSQL. The terminal reported an invalid SSL mode value.

My PostgreSQL connection URL was stored in an ignored .env file, so I needed help investigating the problem without sharing the complete URL or any credentials.

## The prompt

My Streamlit application cannot connect to Azure PostgreSQL. The terminal reports an invalid SSL mode value. My connection URL is stored in an ignored .env file.

## The response

ChatGPT explained that the error was probably caused by an incorrect SSL setting in the PostgreSQL URL. It advised me to check that the URL in my local .env file ended with:

?sslmode=require

## Reflection

I checked the connection URL in my .env file and discovered that I had written:

?sslmode=requir

The final letter e was missing. I corrected it to:

?sslmode=require

After saving the .env file and restarting Streamlit, the application connected successfully to Azure PostgreSQL and loaded the dashboard.

From this error, I learned to pay closer attention when copying connection URLs and configuration values. Even a small typo can prevent an application from connecting, so I should carefully compare copied values with the original instructions before running the application.

---

> Remember: never paste real connection strings, passwords, or PII into an LLM.
> The NYC TLC dataset is public so sample rows are safe here, but practise the habit.
