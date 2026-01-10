# Incident Report: Database Connection Pool Exhaustion

## Executive Summary
Production database experienced connection pool exhaustion at 14:45 UTC, resulting in 500 errors for approximately 30 minutes. Root cause identified as misconfigured cron job creating excessive connections. Issue resolved by restarting database and adjusting connection pool settings. No data loss occurred.

## Affected Systems
- Production Database (PostgreSQL)
- API Gateway
- User Authentication Service
- Order Processing System

## Timeline
**14:45** - First user reports of 500 errors begin [critical]
**14:47** - Monitoring alerts triggered for database connection pool
**14:50** - On-call engineer Dave notified via PagerDuty
**14:52** - Database logs show connection pool at 100% capacity
**15:00** - Identified rogue cron job creating 200+ connections
**15:05** - Cron job disabled, database restarted
**15:10** - Connection pool recovered to normal levels
**15:15** - All services confirmed operational, errors ceased

## Root Cause Analysis
A newly deployed cron job (deployed 13:00 UTC) for data export was misconfigured to create a new database connection for each row processed rather than reusing a single connection. With 50,000 rows to process every hour, this exhausted the connection pool limit of 200 connections within 90 minutes of deployment.

The issue was not caught in staging because staging database has unlimited connections and test dataset only contained 100 rows.

## Impact Assessment
- **Duration**: 30 minutes of degraded service (14:45-15:15 UTC)
- **Users Affected**: Approximately 2,500 users unable to login or complete transactions
- **Failed Transactions**: 847 orders failed, users notified to retry
- **Revenue Impact**: Estimated $12,000 in delayed transactions (all recovered)
- **Data Integrity**: No data loss or corruption

## Resolution
1. Disabled problematic cron job via admin panel
2. Restarted PostgreSQL database service to clear hung connections
3. Increased connection pool maximum from 200 to 300 (temporary)
4. Verified service recovery across all dependent systems
5. Monitored for 2 hours post-incident to ensure stability

## Action Items
1. **[high]** Refactor cron job to use connection pooling (Assigned: Dave)
2. **[high]** Add connection pool monitoring alerts at 70% threshold (Assigned: SRE Team)
3. **[medium]** Update staging environment to mirror production connection limits
4. **[medium]** Implement connection leak detection in application code
5. **[low]** Review all other cron jobs for similar patterns
6. **[low]** Document connection management best practices for team

## Related Incidents
- INC-2024-0089 - Similar connection pool issue in staging (2024-03-15)
- INC-2024-0034 - Database performance degradation (2024-02-01)
