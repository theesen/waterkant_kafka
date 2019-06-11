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

> Summary: 30
# Part 2: Ksql
4. KSQL
    - duration: 15
> me: Explain Basic Commands of KSQL  
> RUN select from stream  
```sql
CREATE STREAM waterkantsql 
    (name VARCHAR
     , workshop VARCHAR
     , value INTEGER) 
WITH (KAFKA_TOPIC='waterkant'
    , VALUE_FORMAT='JSON');

SELECT * FROM waterkantsql;
```
> CREATE TABLE FROM stream  
```sql

```

> Summary: 15  
> Total: 45

## mytodo:
1. setup docker env
* confluent kafka
* producer service
* consumer service
* kafkaManager
* ksql server
* add kafkacat node

2. write documentation and detailed steps + commands

3. publish and test

3. print handouts