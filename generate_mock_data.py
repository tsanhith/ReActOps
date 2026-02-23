#!/usr/bin/env python
"""
Script to generate mock data for ReActOps.
Run this once to populate the data/ directory.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Define base directory (where this script is located)
BASE_DIR = Path(__file__).parent

# Paths to data subfolders
RUNBOOKS_DIR = BASE_DIR / "data" / "runbooks"
TICKETS_DIR = BASE_DIR / "data" / "tickets"
LOGS_FILE = BASE_DIR / "data" / "logs.txt"

# Create directories if they don't exist
RUNBOOKS_DIR.mkdir(parents=True, exist_ok=True)
TICKETS_DIR.mkdir(parents=True, exist_ok=True)

# -------------------- Runbooks --------------------
# Each runbook is a dictionary with metadata and content
runbooks = [
    {
        "title": "Database Connection Failure",
        "last_reviewed": "2024-01-15",
        "applies_to": "payment-service, inventory-service",
        "content": """
## Symptoms
- Payment service reports 'database timeout'
- Connection pool exhaustion errors

## Steps
1. Check database server health: `ping db.internal`
2. Verify connection limits: `SHOW max_connections;`
3. Restart database service: `sudo systemctl restart postgresql`
4. If problem persists, increase connection pool size in config.
"""
    },
    {
        "title": "High CPU Usage on Application Server",
        "last_reviewed": "2023-11-20",
        "applies_to": "web-server, api-server",
        "content": """
## Symptoms
- CPU > 90% for extended period
- Slow response times

## Steps
1. Identify top processes: `top -b -n 1 | head -20`
2. Check for unusual process names or resource leaks.
3. Restart the application service: `sudo systemctl restart myapp`
4. If recurring, consider scaling horizontally.
"""
    },
    {
        "title": "API Timeout Errors",
        "last_reviewed": "2024-02-01",
        "applies_to": "api-gateway",
        "content": """
## Symptoms
- Clients receive 504 Gateway Timeout
- Upstream service slow to respond

## Steps
1. Check upstream service logs for latency.
2. Verify timeout settings in nginx/AWS ALB.
3. Increase timeout temporarily if needed.
4. Investigate if upstream is overwhelmed.
"""
    },
    # Add two more runbooks for variety
    {
        "title": "Disk Space Full",
        "last_reviewed": "2024-01-10",
        "applies_to": "all-servers",
        "content": """
## Symptoms
- Disk usage alerts
- Services failing to write logs

## Steps
1. Check disk usage: `df -h`
2. Find large files: `du -sh /* 2>/dev/null | sort -h`
3. Clean up old logs: `sudo logrotate -f /etc/logrotate.conf`
4. If necessary, extend the volume.
"""
    },
    {
        "title": "Service Not Starting After Reboot",
        "last_reviewed": "2023-12-05",
        "applies_to": "payment-service",
        "content": """
## Symptoms
- Service fails to start automatically after reboot
- Manual start works

## Steps
1. Check if service is enabled: `systemctl is-enabled payment-service`
2. Enable it: `sudo systemctl enable payment-service`
3. Check logs for startup errors: `journalctl -u payment-service -b`
"""
    }
]

# Loop through each runbook and write to a separate Markdown file
for i, rb in enumerate(runbooks, start=1):
    # Create filename like runbook_001.md
    filename = RUNBOOKS_DIR / f"runbook_{i:03d}.md"
    with open(filename, "w", encoding="utf-8") as f:
        # Write YAML frontmatter (metadata between --- lines)
        f.write("---\n")
        f.write(f"title: {rb['title']}\n")
        f.write(f"last_reviewed: {rb['last_reviewed']}\n")
        f.write(f"applies_to: {rb['applies_to']}\n")
        f.write("---\n\n")
        # Write the main content
        f.write(rb['content'].strip())
    print(f"Created {filename}")

print(f"Generated {len(runbooks)} runbooks.")

# -------------------- Logs --------------------
# We'll generate 500 random log lines over the last 7 days
services = ["payment-service", "inventory-service", "api-gateway", "web-server"]
levels = ["INFO", "WARN", "ERROR"]
messages = [
    "Database connection timeout",
    "CPU usage at 95%",
    "Request completed successfully",
    "Failed to connect to redis",
    "Slow query detected (5.2s)",
    "Service restarted",
    "Out of memory",
    "Disk space low",
]

with open(LOGS_FILE, "w", encoding="utf-8") as f:
    for _ in range(500):
        # Random timestamp within the last 7 days (10080 minutes)
        minutes_ago = random.randint(0, 10080)
        timestamp = datetime.now() - timedelta(minutes=minutes_ago)
        # ISO format timestamp
        timestamp_str = timestamp.isoformat(sep=' ', timespec='seconds')
        service = random.choice(services)
        # Weighted random: 70% INFO, 20% WARN, 10% ERROR
        level = random.choices(levels, weights=[0.7, 0.2, 0.1])[0]
        msg = random.choice(messages)
        log_line = f"{timestamp_str} | {service} | {level} | {msg}\n"
        f.write(log_line)
print(f"Generated 500 log lines in {LOGS_FILE}")

# -------------------- Tickets --------------------
tickets = [
    {
        "id": "INC-001",
        "title": "Payment service database timeout",
        "date": "2025-01-10",
        "description": "At 10:15 UTC, payment service became unresponsive. Logs showed connection pool exhaustion.",
        "resolution": "Increased max connections from 100 to 200."
    },
    {
        "id": "INC-002",
        "title": "High CPU on web servers",
        "date": "2025-01-22",
        "description": "CPU spiked to 98% on two web servers. Top showed many php-fpm processes.",
        "resolution": "Tuned php-fpm pm settings and added another server to the pool."
    },
    {
        "id": "INC-003",
        "title": "API gateway timeout after deploy",
        "date": "2025-02-05",
        "description": "After deploying new version, API gateway returned 504 for 10 minutes.",
        "resolution": "Rolled back deployment; issue was due to misconfigured timeout in code."
    },
]

for ticket in tickets:
    filename = TICKETS_DIR / f"{ticket['id']}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(ticket, f, indent=2)
    print(f"Created {filename}")

print("Mock data generation complete.")