# AI Conversational BI Agent

## Overview
This project is an AI-powered BI agent that converts natural language queries into SQL, executes them on an e-commerce dataset using DuckDB, and returns results with visualizations and insights.

## How to Run
```
pip install -r requirements.txt
ollama pull llama3
ollama pull sqlcoder
streamlit run app.py
```

## Architecture Overview
User Query  
↓  
AI Agent (Llama3 - reasoning)  
↓  
SQL Generator (SQLCoder)  
↓  
DuckDB (execution engine)  
↓  
Error Correction (retry mechanism)  
↓  
Insight Generator (Llama3)  
↓  
Visualization (chart)

## Design Decisions
- DuckDB used for efficient analytical queries on large datasets
- Hybrid model: Llama3 for reasoning, SQLCoder for SQL generation
- Agent-based architecture enables tool usage and flexible reasoning
- Retry mechanism improves reliability of SQL execution

## Limitations
- LLM-generated SQL may fail for complex queries
- Performance depends on query complexity
- Requires local models via Ollama

## Failure Handling
- SQL errors are captured and corrected using a retry mechanism
- If visualization fails, system still returns tabular output
