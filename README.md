# sre-tools

An ongoing project meant to aid monitoring and operations.

## Features

- **Health Check** — performs GET requests to confirm URL availability, returns response time, and includes retries to reduce false positives
- **Log Analysis** — tallies INFO, WARNING, and ERROR entries from a log file, and identifies incident start and end times
- **API Check** — validates a URL's JSON API response against an expected field and value
- **Ping Test** — performs ICMP ping tests and returns response time

## Usage

Run via command line using the following flags:

```bash
python sre_tool.py --check       # HTTP health check
python sre_tool.py --logs        # Log file analysis
python sre_tool.py --api         # API response check
python sre_tool.py --report      # Combined shift report
python sre_tool.py --ping        # Ping test
```

Append `--teams` to any flag to send the result to a Teams channel via webhook:

```bash
python sre_tool.py --check --teams
```

## Setup

1. Clone the repository
2. Copy `config.example.json` to `config.json` and fill in your targets
3. Set the following environment variable: