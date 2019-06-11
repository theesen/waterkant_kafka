# Content
## Part 1: kafka basics
0. Introduction
    - duration: 7  
    - prepare: What is Kafka,  
    Why we use kafka
> me: Introduction into workshop, introduce myself and what I am doing
> me: Show architecture overview (search for picture of architecture)  
> 2min: Sample useCases (real time monitoring, metric collection & aggregation, data offloading)  

1. Install and Run Kafka 
    - duration: 5 + 5  
> me: Walk through docker-compose file, share link to github repo
> Task: Everybody needs to launch kafka successfully docker-compose
```sh
docker-compose logs kafka | grep started
```
> Task: Create a Topic
```sh
docker-compose exec kafka kafka-topics --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 3 --topic waterkant
```

2. Pub messages using kafka sample producer
    - duration: 5 + 10
    - prepare: Walk through sample python producer  
    Consume Events using cli  
    Consume Events using python app  
> me: Walk through python producer  
> me: enable kafkaproducer in docker-compose
> launch producer
```sh
docker-compose up --build -d
```
> Check out Producer Logs
```sh
docker-compose logs -f kafkaproducer
```
> use kafkacat to consume messages (add command to documentation)  
```sh
#list topics & partitions
docker run --tty \
           --network waterkant_kafka_default \
           confluentinc/cp-kafkacat \
           kafkacat -b kafka:29092 \
                    -L

#consume messages
docker run --tty \
           --network waterkant_kafka_default \
           confluentinc/cp-kafkacat \
           kafkacat -b kafka:29092 \
                    -C -t waterkant
```

> Summary: 30
# Part 2: Ksql
4. KSQL
    - duration: 15
> me: Explain Basic Commands of KSQL  
> RUN select from stream  
```sh
# launch ksql-cli
docker-compose exec ksql-cli ksql http://ksql-server:8088
```
```sql
# create ksql stream
CREATE STREAM waterkantsql 
    (name VARCHAR
     , workshop VARCHAR
     , value INTEGER) 
WITH (KAFKA_TOPIC='waterkant'
    , VALUE_FORMAT='JSON');

# describe ksql stream
DESCRIBE EXTENDED waterkantsql;

# stream events from ksql
SELECT * FROM waterkantsql;
```
> CREATE TABLE FROM stream  
```sql
CREATE TABLE waterkant_agg AS
  SELECT rowkey,
         COUNT(*)
  FROM waterkantsql
  GROUP BY rowkey;

SELECT * FROM waterkant_agg;
```
> Play around with some aggregation options:
* Where clauses
* Window functions
Examples:
https://docs.confluent.io/current/ksql/docs/developer-guide/aggregate-streaming-data.html

> Summary: 15  
> Total: 45

## mytodo:
<!-- 1. setup docker env -->
<!-- * confluent kafka -->
<!-- * producer service -->
<!-- * consumer service -->
* kafkaManager
<!-- * ksql server -->
<!-- * add kafkacat node -->

2. write documentation and detailed steps + commands

3. publish and test

3. print handouts