This project presents an AI-powered Conversational Business Intelligence (BI) Agent designed to simplify data analysis for non-technical users. The system allows users to ask questions in natural language and automatically generates SQL queries, executes them on a large e-commerce dataset, and returns both tabular results and visual insights.

The solution follows an agent-based architecture, where a reasoning model interprets user queries and orchestrates multiple tools such as SQL generation, query execution, error correction, and insight generation.

A hybrid model approach is used:

A reasoning model handles query understanding and decision-making
A specialized SQL model generates accurate SQL queries

The system uses DuckDB as the execution engine to efficiently process large datasets and perform complex multi-table joins.

Additionally, the system includes:

Self-correcting SQL mechanism to handle query failures
Automatic chart generation (bar, line, pie) based on result type
Business insight generation to translate raw data into meaningful conclusions

Overall, this project demonstrates how AI agents can be used to build scalable, intelligent, and user-friendly data analytics systems.
