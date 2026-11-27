# Project 06 specification: big data processing and optimisation

**Status:** Not started. **Domain:** digital platform (clickstream and transactions).

## Scenario
Batch jobs over event and transaction data slow down sharply as volume grows. The project
investigates why and which optimisations actually help, on a single machine.

## Experiments (each isolates one variable)
1. File layout: many small files vs compacted Parquet vs Delta `OPTIMIZE`.
2. Partitioning: none vs date vs date+region; effect on selective queries (partition pruning).
3. Predicate pushdown: Parquet filter on sorted vs unsorted data.
4. Joins: sort-merge vs broadcast; effect of skew and of AQE on or off.
5. Shuffle: `spark.sql.shuffle.partitions` sweep; repartition vs coalesce.
6. Caching: with and without `cache()` for a reused intermediate result.
7. Memory: executor/driver memory settings and spill observations.

## Acceptance criteria
1. One command runs the suite end to end and writes raw JSON/CSV results plus a summary.
2. Each experiment reports data volume, configuration, iterations, median and min/max, and the Spark
   physical plan or metric that explains the result.
3. Experiments that show no improvement are reported as such.
4. The README lists the machine used and states that results are single-node and not extrapolated.

## Out of scope
Cluster-scale claims; cost modelling for cloud Spark.
