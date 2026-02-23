---
title: Database Connection Failure
last_reviewed: 2024-01-15
applies_to: payment-service, inventory-service
---

## Symptoms
- Payment service reports 'database timeout'
- Connection pool exhaustion errors

## Steps
1. Check database server health: `ping db.internal`
2. Verify connection limits: `SHOW max_connections;`
3. Restart database service: `sudo systemctl restart postgresql`
4. If problem persists, increase connection pool size in config.