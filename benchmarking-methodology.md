# Benchmarking methodology

Applies to every project that reports performance, latency, throughput or cost.

## Rules

1. **Repeatable.** A single command (for example `make benchmark`) reproduces the run.
   The data generator is seeded; the seed is recorded.
2. **Controlled.** Each experiment changes one variable. The baseline is the naive
   approach, run under identical conditions.
3. **Statistically honest.** Run at least 5 measured iterations after 1-2 warm-up runs;
   report median and min/max (or p95 where relevant), not a single best run.
4. **Fully described.** Record CPU count, memory, storage type, OS, tool versions,
   container limits and data volume (rows and bytes) with every result.
5. **Raw output is committed.** Results are written as JSON/CSV under
   `<project>/benchmarks/results/` together with a short Markdown summary.
6. **Limits are stated.** Laptop-scale results are labelled as such and are not
   extrapolated to cluster or production workloads.
7. **No invented improvements.** If an optimisation does not help, the result is
   published as is.

## Result record (minimum fields)

```json
{
  "experiment": "broadcast-join-vs-shuffle-join",
  "seed": 42,
  "environment": {"cpus": 0, "memory_gb": 0, "os": "", "spark": "", "python": ""},
  "data": {"rows": 0, "size_bytes": 0},
  "iterations": 5,
  "seconds": {"median": 0.0, "min": 0.0, "max": 0.0}
}
```

The zeros above are the schema, not results.
