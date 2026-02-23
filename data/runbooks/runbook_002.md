---
title: High CPU Usage on Application Server
last_reviewed: 2023-11-20
applies_to: web-server, api-server
---

## Symptoms
- CPU > 90% for extended period
- Slow response times

## Steps
1. Identify top processes: `top -b -n 1 | head -20`
2. Check for unusual process names or resource leaks.
3. Restart the application service: `sudo systemctl restart myapp`
4. If recurring, consider scaling horizontally.