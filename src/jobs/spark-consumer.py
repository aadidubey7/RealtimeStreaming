from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, StructField, FloatType
from pyspark.sql.functions import col, from_json, to_json, struct, udf, when
from config.config import config
import openai

import time

def sentiment_analysis(comment) -> str:
    if comment:
        # since the openai api version is not compatible and giving an error
        # therefore skipping the open-ai call as of now I will add this logic later on
        pass
        # openai.api_key = config["openai"]["api_key"]
        # completion = openai.ChatCompletion.create(
        #     model='gpt-3.5-turbo',
        #     message=[
        #         {
        #             "role": "system",
        #             "content": """
        #                 You are a machine learning model with a task of classifying comments into POSITIVE, NEGATIVE, NEUTRAL.
        #                 YOU are to respond with one word from the option specified above, do not add anything else.
        #                 Here is the comment:
        #
        #                 {comment}
        #             """.format(comment=comment)
        #         }
        #     ]
        # )
        # return completion.choices[0].message['content']
    return "Empty"

def start_consume(spark):
    while True:
        try:
            stream_df = (
                spark.readStream.format('socket')
                .option('host', '0.0.0.0')
                .option('port', 9999)
                .load()
            )

            schema = StructType([
                StructField('review_id', StringType()),
                StructField('user_id', StringType()),
                StructField('business_id', StringType()),
                StructField('stars', FloatType()),
                StructField('date', StringType()),
                StructField('text', StringType()),
            ])

            stream_df = stream_df.select(from_json(col('value'), schema=schema).alias('data')).select(('data.*'))

            # call openai to perform sentiment analysis on comments
            sentiment_analysis_udf = udf(sentiment_analysis, StringType())

            df_with_sentiment_analysis = stream_df.withColumn(
                "feedback",
                when(col('text').isNotNull(), sentiment_analysis_udf(col('text'))).otherwise(None)
            )

            # writing data to kafka
            kafka_df = df_with_sentiment_analysis.selectExpr("CAST(review_id as STRING) AS key", "to_json(struct(*)) AS value")

            query = (
                kafka_df.writeStream.format('kafka')
                .option('kafka.bootstrap.servers', config['kafka_confluent_cloud']['bootstrap.server'])
                .option('kafka.security.protocol', config['kafka_confluent_cloud']['security.protocol'])
                .option('kafka.sasl.mechanism', config['kafka_confluent_cloud']['sasl.mechanisms'])
                .option(
                    'kafka.sasl.jaas.config',
                    'org.apache.kafka.common.security.plain.PlainLoginModule required username="{username}" password="{password}"; '.format(
                        username = config['kafka_confluent_cloud']['sasl.username'],
                        password = config['kafka_confluent_cloud']['sasl.password']
                    )
                )
                .option('checkpointLocation', '/tmp/checkpoint')
                .option('topic', config['kafka_confluent_cloud']['topic'])
                .start()
                .awaitTermination()
            )

        except Exception as e:
            print(f'Exception encountered {e} Retrying in 10 seconds')
            time.sleep(10)

if __name__ == '__main__':
    spark_conn = SparkSession.builder.appName('SocketStreamingConsumer').getOrCreate()

    start_consume(spark_conn)
