from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType,LongType,TimestampType
from pyspark.sql.functions import from_json, explode, count,struct, desc, asc, row_number,col,to_timestamp,window,expr,to_json

def price_change_24_hr(curr_price, open_24h,):
    return  ((curr_price-open_24h)/open_24h) * 100

def main ():
    spark = SparkSession \
        .builder \
        .appName("crypto-streaming-analyzer") \
        .getOrCreate()
    
    spark.sparkContext.setLogLevel('WARN')

    # Define the schema for JSON messages
    schema = StructType([
        StructField("type", StringType(), True),
        StructField("sequence", LongType(), True),
        StructField("product_id", StringType(), True),
        StructField("price", StringType(), True),
        StructField("open_24h", StringType(), True),
        StructField("volume_24h", StringType(), True),
        StructField("low_24h", StringType(), True),
        StructField("high_24h", StringType(), True),
        StructField("volume_30d", StringType(), True),
        StructField("best_bid", StringType(), True),
        StructField("best_bid_size", StringType(), True),
        StructField("best_ask", StringType(), True),
        StructField("best_ask_size", StringType(), True),
        StructField("side", StringType(), True),
        StructField("time", StringType(), True),
        StructField("trade_id", LongType(), True),
        StructField("last_size", StringType(), True)
    ])

    df =  spark \
        .readStream \
        .format('kafka') \
        .option("kafka.bootstrap.servers", "localhost:9094") \
        .option("subscribe", "crypto.coinbase.ticker") \
        .load()
    
    
    
    json_data = df.selectExpr("CAST(value AS STRING) as json")
    df = json_data.select(from_json(json_data["json"], schema).alias("data"))


    # Apply watermarking based on an event time column (e.g., timestamp_column)
    streaming_df = df.withColumn('event_time', to_timestamp('data.time'))\
        .withColumn('price_change_24hr', price_change_24_hr(df.data.price, df.data.open_24h)) \
        .withWatermark("event_time", "6 minutes")

    # aggregate min price, max price , latest time and latest price.
    exp = [expr("min(data.price)"), expr("max(data.price)"), expr("last(event_time)"),expr("last(data.price)"),expr("last(price_change_24hr)")]

    # event time window into 5 mins, group by product_id
    window_df = streaming_df.groupBy(
        window(streaming_df.event_time , "5 minutes"),col("data.product_id")
    ).agg(*exp)

    window_df = window_df.withColumnRenamed("min(data.price)", "min_data_price")\
                .withColumnRenamed("max(data.price)", "max_data_price")\
                .withColumnRenamed("last(event_time)", "latest_event_time") \
                .withColumnRenamed("last(data.price)","curr_price") \
                .withColumnRenamed("last(price_change_24hr)","price_change_24hr")

    window_df.printSchema()

    window_df = window_df.withColumn("value",
                                      to_json(struct([window_df.window.start,
                                                             window_df.window.end,
                                                             window_df.product_id,
                                                             window_df.min_data_price,
                                                             window_df.max_data_price,
                                                             window_df.latest_event_time,
                                                             window_df.curr_price,
                                                             window_df.price_change_24hr
                                                             ] )))


    out = window_df.writeStream \
        .outputMode('update')\
        .format('console') \
        .start()

    out = window_df.writeStream \
        .outputMode('update') \
        .format('kafka') \
        .option("kafka.bootstrap.servers", "localhost:9094") \
        .option("checkpointLocation","/tmp/chkpoint2") \
        .option("topic", "crypto.price.updates") \
        .start()
    #
        

    out.awaitTermination()

if __name__ == '__main__':
    main()
    

    