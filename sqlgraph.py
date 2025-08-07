#!/usr/bin/env python3
"""
Simple SQL ETL Analyzer - POC Version
"""

import sqlglot
import ollama
import sys

def analyze_sql_file(file_path, model="hf.co/unsloth/gemma-3n-E4B-it-GGUF:UD-Q4_K_XL"):
    # Read SQL file
    with open(file_path, 'r') as f:
        sql_content = f.read()

    # Parse SQL statements
    statements = sqlglot.parse(sql_content)

    # Initialize Ollama client
    client = ollama.Client()
    output = [] 
    # Analyze each statement
    for i, stmt in enumerate(statements, 1):
        if stmt is None:
            continue

        print(f"\n=== Statement {i} ===")
        print(f"Type: {stmt.__class__.__name__}")
        print(f"SQL: {str(stmt)[:100]}...")

        # Create prompt
        prompt = f"""
Given the following SQL statement:

{str(stmt)}

Identify all table names used in the SQL statement.

For each table:

If the table is a source (used in SELECT, FROM, JOIN, etc.), format as: inbound.table_name

If the table is a target (used in INSERT INTO, MERGE INTO, UPDATE, DELETE FROM), format as: outbound.table_name

If multiple tables, output them as a list separated by the \n character, one per line.

Only output the formatted table names. Do not include any additional explanation.
"""

        # Query Ollama
        response = client.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )

        # print("Analysis:")
        output += response["message"]["content"].split("\n")
        print(response["message"]["content"].split("\n"))
        # print("-" * 50)
    print(set(output))
if __name__ == "__main__":
    # if len(sys.argv) != 2:
        # print("Usage: python sql_analyzer.py <sql_file>")
        # sys.exit(1)
    pth = "test.sql" 
    analyze_sql_file(pth)
