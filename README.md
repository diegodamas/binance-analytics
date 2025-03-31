# Apache Flink Binance Analytics with Elasticsearch

This repository contains an Apache Flink application for analytics built using Docker Compose to orchestrate the necessary infrastructure components, including Apache Flink and Elasticsearch. The application processes data from Kafka, performs aggregations, and stores the results in Elasticsearch for further analysis.

## Requirements
- Docker
- Docker Compose

## Installation and Setup
1. Clone this repository.
2. Navigate to the repository directory.
3. Run `docker-compose up` to start the required services (Apache Flink, Elasticsearch).
4. The Transaction Generator `main.py` helps to generate the transactions into Kafka.