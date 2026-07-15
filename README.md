# Neo4jUtils

A collection of documentation, scripts, metrics, and utilities for working with [Neo4j](https://neo4j.com/) and graph databases more broadly. This repo is meant to be a living toolbox — practical runbooks, infrastructure references, analysis scripts, and reusable code for anyone standing up, maintaining, or building on top of Neo4j.

## Contents

```
Neo4jUtils/
├── career/        # Job descriptions, skill requirements, hiring/screening guides
├── installation/  # Installation guides, configs, and prerequisites
├── metrics/        # Graph metrics, scoring models, and analysis utilities
├── scripts/        # Handy scripts (Python, Cypher, shell, etc.)
├── docs/           # General reference docs, architecture notes, glossaries
└── research/       # Exploratory notes, benchmarks, papers, and experiments
```

### `career/`
Job descriptions, required-skills matrices, and interview/screening guides for Neo4j- and Linkurious-adjacent roles (e.g. sysadmin/maintainer vs. graph data engineer vs. full-stack graph developer). Useful for scoping hires or clarifying role boundaries.

### `installation/`
Step-by-step installation and provisioning guides, sample configuration files (`neo4j.conf`, systemd units, etc.), and infrastructure prerequisites — covering topics like AWS EC2 sizing, OS/JVM requirements, storage layout, networking/security group rules, and companion tooling (e.g. Linkurious Enterprise).

### `metrics/`
Graph-analytics and scoring code — gravity models, Huff-style probability models, entropy weighting, and other quantitative approaches to analyzing graph/store/customer data. Includes both production-style utilities and exploratory/prototype scripts.

### `scripts/`
Standalone utility scripts for day-to-day Neo4j operations: exporting indexes/constraints, backup helpers, health-check queries, data loaders, and reusable Cypher snippets.

### `docs/`
General-purpose reference material that doesn't fit neatly into installation or career docs — architecture diagrams, glossaries of graph-database terminology, troubleshooting guides, and internal standards/conventions.

### `research/`
Exploratory work: benchmarking notes, algorithm comparisons, proof-of-concept models, and links to or summaries of external papers/blog posts relevant to graph databases.

> Directory structure is expected to evolve. New top-level folders should be added here as they're introduced.

## Getting Started

Most scripts in this repo assume you have:

- Python 3.9+ (for scripts in `scripts/` and `metrics/`)
- The official [`neo4j` Python driver](https://pypi.org/project/neo4j/) (`pip install neo4j`)
- Access to a running Neo4j instance (local, Docker, or cloud-hosted)

Connection details for Python scripts are generally read from environment variables:

```bash
export NEO4J_URI="bolt://localhost:7687"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-password"
export NEO4J_DATABASE="neo4j"
```

Check each script's header/docstring for specific requirements and usage instructions.

## Contributing

This is primarily a personal/team knowledge base, but contributions, corrections, and additional utilities are welcome. When adding new material:

- Place it in the most relevant existing directory, or propose a new top-level directory if it doesn't fit.
- Include a short header/docstring explaining purpose, prerequisites, and usage for any script.
- Prefer environment variables over hardcoded credentials in any code that connects to a live database.

## MIT License

Copyright (c) 2026 Kovach Technologies

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


## Disclaimer

Configuration values, instance sizes, and version numbers referenced in this repo (e.g. specific AWS instance types, memory settings) are starting points based on particular workloads and should be validated against your own graph size, query patterns, and infrastructure before use in production.
