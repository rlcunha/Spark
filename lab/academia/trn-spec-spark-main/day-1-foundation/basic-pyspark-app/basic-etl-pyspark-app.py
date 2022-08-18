# import libraries
from pyspark.sql import SparkSession
from pyspark import SparkConf

# begin code 
if __name__ == '__main__':
    
    # init spark app
    spark = SparkSession \
        .builder \
        .appName("basic-etl-pyspark-app") \
        .getOrCreate()
    
    # dataframe = user
    df_user = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json("/Users/luanmorenomaciel/GitHub/trn-spec-spark/files/landing-zone/user/*.json")
    
    # dataframe = subscription
    df_subscription = spark.read \
        .format("json") \
        .option("inferSchema", "true") \
        .option("header", "true") \
        .json("/Users/luanmorenomaciel/GitHub/trn-spec-spark/files/landing-zone/subscription/*.json")
        
    # print
    df_user.printSchema()
    df_subscription.printSchema()
    
    df_user.show()
    df_subscription.show()
