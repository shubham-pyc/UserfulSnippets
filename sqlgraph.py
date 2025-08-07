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
Analyze this SQL statement for ETL purposes:

{str(stmt)}

Given this ETL give me the source table. Only give me the table name. 
If there are multiple tables only give me the table names wiht \n character.
if table is inbound table give it a name inbout.tablename, if table is outbound(insert or merge) give it a name of outbound.tablename
"""

        # Query Ollama
        response = client.chat(
            model=model,
            messages=[{'role': 'user', 'content': prompt}]
        )

        # print("Analysis:")
        output += response["message"]["content"].split("\n")
        # print("-" * 50)
    print(set(output))
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sql_analyzer.py <sql_file>")
        sys.exit(1)
    
    analyze_sql_file(sys.argv[1])
