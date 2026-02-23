---
title: API Timeout Errors
last_reviewed: 2024-02-01
applies_to: api-gateway
---

## Symptoms
- Clients receive 504 Gateway Timeout
- Upstream service slow to respond

## Steps
1. Check upstream service logs for latency.
2. Verify timeout settings in nginx/AWS ALB.
3. Increase timeout temporarily if needed.
4. Investigate if upstream is overwhelmed.