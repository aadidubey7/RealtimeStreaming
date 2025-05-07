
# Realtime Data Streaming With TCP Socket, Apache Spark, OpenAI LLM, Kafka and Elasticsearch | End-to-End Data Engineering Project

A scalable ETL pipeline for streaming data from socket and push it to kafka cluster.


## Table of Contents

- Overview
- Architecture
- What We Learn
- Technologies
- System Setup
- Project Demo

## Overview

This project serves as a comprehensive guide to building an end-to-end data engineering pipeline using TCP/IP Socket, Apache Spark, OpenAI LLM, Kafka and Elasticsearch. It covers each stage from data acquisition, processing, sentiment analysis with ChatGPT, production to kafka topic and connection to elasticsearch.

## Architecture
    ![Project Architecture](System_architecture.png)
    
        
        
    The project is designed with the following components:
    - Data Source: We use yelp.com dataset for our pipeline.
    - TCP/IP Socket: Used to stream data over the network in chunks
    - Apache Spark: For data processing with its master and worker nodes.
    - Confluent Kafka: Our cluster on the cloud
    - Control Center and Schema Registry: Helps in monitoring and schema management of our Kafka streams.
    - Kafka Connect: For connecting to elasticsearch
    - Elasticsearch: For indexing and querying

## What We Learn

- Setting up data pipeline with TCP/IP
- Real-time data streaming with Apache Kafka
- Data processing techniques with Apache Spark
- Realtime sentiment analysis with OpenAI ChatGPT
- Synchronising data from kafka to elasticsearch
- Indexing and Querying data on elasticsearch

## Technologies
- Python
- TCP/IP
- Confluent Kafka
- Apache Spark
- Docker
- Elasticsearch

## System Setup
- Clone the repository

    
        git clone https://github.com/aadidubey7/RedditDataEngineering.git
        
- Create a virtual environment
        
        python3 -m venv .venv

- Activate the virtual environment

        .\.venv\Scripts\activate

- Install the dependencies

        pip install -r requirements.txt

- Add your credentials in the config/config.py file. However, storing credentials in a file is not recommended. Instead, use environment variables for better security.

- Starting the containers
        
        docker-compose up -d

- Go to docker container bash.

        docker exec -it spark-master /bin/bash

- Run the socket streaming file

        python jobs/socket-streaming.py

- Submit spark job from the container

        docker exec -it spark-master spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 jobs/spark-consumer.py
