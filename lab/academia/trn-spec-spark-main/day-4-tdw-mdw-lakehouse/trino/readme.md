# Data Virtualization using Trino & MinIO [Data Lake]

### connecting ingo trino coordinator [master]
```sh
# info to connect
kubectx aks-owshq-orion-dev

kubens processing
# trino info [config]
kgp

# access coordinator
TRINO=trino-coordinator-54dc8d4c67-lrqm9
kubectl exec $TRINO -it -- /usr/bin/trino
```

### virtualized queries using minio [s3]
```sql
-- show minio storage
-- http://20.72.90.44:9000/

-- list catalogs
show catalogs;

-- create schema
-- drop table if exists
CREATE SCHEMA minio.files;
DROP TABLE minio.files.ds_gold_reviews_full_parquet;
DROP TABLE minio.files.ds_gold_reviews_full_orc;

-- creating table from [parquet] files
CREATE TABLE minio.files.ds_gold_reviews_full_parquet
(
  review_id VARCHAR,
  business_id VARCHAR,
  user_id VARCHAR,
  review_stars BIGINT,
  review_useful BIGINT,
  store_name VARCHAR,
  store_city VARCHAR,
  store_state VARCHAR,
  store_category VARCHAR,
  store_review_count BIGINT,
  store_stars DOUBLE,
  user_name VARCHAR,
  user_average_stars DOUBLE,
  user_importance VARCHAR
)
WITH
(
  external_location = 's3a://curated/ds_gold_reviews_full_parquet/',
  format = 'parquet'
);

-- creating table from [orc] files
CREATE TABLE minio.files.ds_gold_reviews_full_orc
(
  review_id VARCHAR,
  business_id VARCHAR,
  user_id VARCHAR,
  review_stars BIGINT,
  review_useful BIGINT,
  store_name VARCHAR,
  store_city VARCHAR,
  store_state VARCHAR,
  store_category VARCHAR,
  store_review_count BIGINT,
  store_stars DOUBLE,
  user_name VARCHAR,
  user_average_stars DOUBLE,
  user_importance VARCHAR
)
WITH
(
  external_location = 's3a://curated/ds_gold_reviews_full_orc/',
  format = 'orc'
);

-- describe data
DESCRIBE minio.files.ds_gold_reviews_full_parquet;
DESCRIBE minio.files.ds_gold_reviews_full_orc;

-- query table
SELECT COUNT(*) AS Q FROM minio.files.ds_gold_reviews_full_parquet;
SELECT COUNT(*) AS Q FROM minio.files.ds_gold_reviews_full_orc;

SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM minio.files.ds_gold_reviews_full_parquet
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC  
LIMIT 10;

SELECT store_name,
    store_city,
    COUNT(*) AS Q
FROM minio.files.ds_gold_reviews_full_orc
WHERE user_importance = 'rockstar'
GROUP BY store_name, store_city
ORDER BY Q DESC  
LIMIT 10;

-- ORC
/*
Query 20210601_222502_00049_gk5bq, FINISHED, 5 nodes
Splits: 226 total, 226 done (100.00%)
35.55 [131M rows, 360MB] [3.69M rows/s, 10.1MB/s]

Query 20210601_222553_00050_gk5bq, FINISHED, 5 nodes
Splits: 226 total, 226 done (100.00%)
32.77 [131M rows, 360MB] [4.01M rows/s, 11MB/s]

Query 20210601_223521_00068_gk5bq, FINISHED, 5 nodes
Splits: 226 total, 226 done (100.00%)
26.84 [131M rows, 360MB] [4.89M rows/s, 13.4MB/s]
*/

-- ui
http://localhost:9000/ui/
```
