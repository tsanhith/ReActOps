---
title: Disk Space Full
last_reviewed: 2024-01-10
applies_to: all-servers
---

## Symptoms
- Disk usage alerts
- Services failing to write logs

## Steps
1. Check disk usage: `df -h`
2. Find large files: `du -sh /* 2>/dev/null | sort -h`
3. Clean up old logs: `sudo logrotate -f /etc/logrotate.conf`
4. If necessary, extend the volume.