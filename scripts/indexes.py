#!/usr/bin/env python3
"""
Export all indexes from a Neo4j server to a CSV file.

The output file is named <today's date>_indexes.csv, e.g. 2026-07-15_indexes.csv,
and is written to the same directory as this script (or a directory you specify).

Requirements:
    pip install neo4j

Usage:
    Set connection details via environment variables (recommended) or edit the
    constants below, then run:

        python export_neo4j_indexes.py

Environment variables:
    NEO4J_URI       e.g. "bolt://localhost:7687" or "neo4j://localhost:7687"
    NEO4J_USER      e.g. "neo4j"
    NEO4J_PASSWORD  e.g. "your-password"
    NEO4J_DATABASE  optional, defaults to "neo4j"
"""

import csv
import os
from datetime import date

from neo4j import GraphDatabase


# 1. Connection settings -----------------------------------------------------
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")
NEO4J_DATABASE = os.environ.get("NEO4J_DATABASE", "neo4j")

# Where to write the CSV. Defaults to the current working directory.
OUTPUT_DIR = os.environ.get("NEO4J_INDEX_CSV_DIR", ".")


def fetch_indexes(driver, database: str):
    """Run SHOW INDEXES and return a list of dicts (one per index)."""
    with driver.session(database=database) as session:
        result = session.run("SHOW INDEXES")
        # result.data() turns each record into a plain dict, keyed by column name
        records = result.data()
    return records


def write_csv(records, output_path: str):
    """Write a list of dicts to a CSV file, one row per record."""
    if not records:
        print("No indexes found — writing an empty CSV with no data rows.")
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return

    # Collect the full set of column names across all records, preserving order
    # of first appearance (some indexes may have slightly different fields).
    fieldnames = []
    for rec in records:
        for key in rec.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in records:
            # Flatten any list/dict values (e.g. labelsOrTypes, properties) into
            # a readable string so they fit cleanly into a CSV cell.
            row = {}
            for key in fieldnames:
                value = rec.get(key)
                if isinstance(value, (list, tuple)):
                    row[key] = "|".join(str(v) for v in value)
                elif isinstance(value, dict):
                    row[key] = str(value)
                else:
                    row[key] = value
            writer.writerow(row)


def main():
    # 2. Connect to the server
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        driver.verify_connectivity()

        # 3 & 4. Execute the cypher command and read the results
        records = fetch_indexes(driver, NEO4J_DATABASE)

        # 5. Build the output filename: YYYY-MM-DD_indexes.csv
        filename = f"{date.today().isoformat()}_indexes.csv"
        output_path = os.path.join(OUTPUT_DIR, filename)

        # 6. Write to CSV
        write_csv(records, output_path)

        print(f"Wrote {len(records)} index record(s) to {output_path}")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
