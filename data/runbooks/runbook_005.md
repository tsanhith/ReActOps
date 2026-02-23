---
title: Service Not Starting After Reboot
last_reviewed: 2023-12-05
applies_to: payment-service
---

## Symptoms
- Service fails to start automatically after reboot
- Manual start works

## Steps
1. Check if service is enabled: `systemctl is-enabled payment-service`
2. Enable it: `sudo systemctl enable payment-service`
3. Check logs for startup errors: `journalctl -u payment-service -b`