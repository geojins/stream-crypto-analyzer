# Learn Stream processing with a real world Data Engineering project

## Overview
Aim of this repository is to  implement a real world stream processing usecase with Crypto Data from Coinbase. The project is implemented with different APIs/engines to familiarize with different styles/processing engines.

## Use Case

# Crypto Data Analysis with Coinbase Market Data

This project demonstrates data engineering skills by analyzing cryptocurrency data from Coinbase Market Data. It includes three use cases with detailed explanations of metrics:

### 1. Real-Time Market Depth Analysis


## Code Structure
### data-ingestion-coinbase-market-data
A python app to consume data from coinbase market data by integrating to coinbase maket data web socket api and publish to one or more kafka topics
### spark-stream-pyspark-crypto-analyzer
Spark streaming App that consumes the coinbase market data  events from kafka and calculate certain metrics. 


## Pre-Requisite
To effectively use this repo, you should have basic understanding of Stream processing, concepts like Windowing, event-time, Java/Python/SQL, Kafka knowledge. 

The project is implemented in Following frameworks/APIs

- Spark Streaming
- Flink
- Beam
  
## Architecture

### Data Ingestion
Coinbase provides real time market data updates for orders and trades via web socket. Data is collected from this API and published to a Kafka topic using a python service. 

## Setup

- Install python 3.10+
- Install Kafka on dokcer - https://hub.docker.com/r/bitnami/kafka
  - docker-compose   -f docker-compose.yml  up --detach
  - update KAFKA_CFG_LISTENERS/KAFKA_CFG_ADVERTISED_LISTENERS/KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP env variables to enable access from external network. 
  - ```
    - KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093,EXTERNAL://:9094
    - KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://:9092,EXTERNAL://localhost:9094
    - KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,EXTERNAL:PLAINTEXT,PLAINTEXT:PLAINTEXT
    - 
    ```
- Create Kafka topics
  -  ./kafka-topics.sh --create --topic crypto.coinbase.ticker  --bootstrap-server localhost:9094