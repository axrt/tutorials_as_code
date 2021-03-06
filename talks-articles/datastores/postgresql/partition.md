
## Partitioning

> source: [dbrnd.com](https://www.dbrnd.com/2017/12/postgresql-10-introduced-native-table-partitioning/)

### Native Table Partitioning in PostgreSQL 10 onwards

* earlier table partition was managed by triggers and check constraints, now it's automatic

* create a table and specify partition column

```
CREATE TABLE mytable (id int GENERATED BY DEFAULT AS IDENTITY, name character varying, created_at timestamp without time zone)
PARTITION BY RANGE (created_at);
```

* create sample partitions with ranges

```
CREATE TABLE mytable_history_201701
PARTITION OF mytable
FOR VALUES FROM ('2017-01-01 00:00:00') TO ('2017-01-31 23:59:59');

CREATE TABLE mytable_history_201702
PARTITION OF mytable
FOR VALUES FROM ('2017-02-01 00:00:00') TO ('2017-02-28 23:59:59');

CREATE TABLE mytable_history_201703
PARTITION OF mytable
FOR VALUES FROM ('2017-03-01 00:00:00') TO ('2017-03-31 23:59:59');
```

* can check main table as `select *From mytable;`

* check individual ranges as

```
select *From mytable_history_201701;
select *From mytable_history_201702;
select *From mytable_history_201703;
```

* version 11 also avails Partition pruning; with it `off` Postgres will scan each partition but when `on` it will scan based on partition definition

```
SET enable_partition_pruning = on;                 -- the default
SET enable_partition_pruning = off;
```

* no longer necessary child tables can be dropped as `DROP TABLE mytable_history_201701;`

* remove child table from inheritance hierarchy `ALTER TABLE mytable_history_201701 NO INHERIT mytable;`

* to add a new child for new data

```
CREATE TABLE mytable_history_201704 (
    CHECK ( created_at >= DATE '2007-04-01' AND created_at < DATE '2007-04-30' )
) INHERITS (mytable);
```

---
