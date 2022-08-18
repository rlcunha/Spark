# Azure Synapse Analytics - Apache Spark Pools

> * deployment option = arm templates & terraform
> * workspace = pythiansynapseworkspace
> * spark pools = pythian
 
## submit job to spark cluster

```sh
# develop area = apache spark job definition
# language = pyspark [python]
# job name = synapse-spark-pools-batch-etl-yelp-py
# main file = abfss://bs-stg-files@owshqblobstg.dfs.core.windows.net/app/synapse/cluster.py

# apache spark pool = owshq
# version = 3.2
# executor size = medium [8 vcores & 64 gb of ram] 
# executors = 3~5
# enable = dynamic allocation
# intelligent cache = %

# submit job to execution
# monitoring web interface ~ monitor -> apache spark applications
```

## total time spent

```sh
# time taken to process
27m 50s
```