# Project 03 specification: real-time streaming platform

**Status:** Not started. **Domain:** last-mile delivery marketplace (orders, courier GPS pings, status events).

## Scenario
Operations must see delivery delays, order volume and courier utilisation within seconds,
despite out-of-order and duplicated events from mobile apps.

## Scope
- Kafka (KRaft) with Python producers (seeded event simulator) and consumers.
- Event schemas with validation; invalid events go to a dead-letter topic.
- Spark Structured Streaming: event-time windows, watermarks, late-event handling,
  deduplication by event id within the watermark, checkpointing, restart recovery.
- Sink: PostgreSQL tables for 1-minute operational aggregates and delay alerts.
- Monitoring: throughput, consumer lag and processing-latency metrics exposed and logged.

## Acceptance criteria
1. Simulator injects a known percentage of duplicates, late and malformed events; outputs match
   a batch recomputation of the same events (correctness test).
2. Killing and restarting the Spark job resumes from checkpoint without losing or double-counting
   events (failure-scenario test).
3. Latency (event time -> row visible in PostgreSQL) and throughput are measured at defined
   event rates on stated hardware; p50/p95 reported with raw data.

## Delivery semantics (to be documented precisely)
At-least-once from Kafka; effectively-once into PostgreSQL through idempotent upserts keyed on
(window, dimension). Not claimed: end-to-end exactly-once transactions.

## Out of scope
Schema registry/Avro (documented as a future improvement), multi-broker clusters.
