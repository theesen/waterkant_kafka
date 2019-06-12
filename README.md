# Part 1: Launch Kafka
In the first part of our workshop we will launch a fresh kafka cluster on our local docker environment.
So make sure that you have docker installed and it has sufficient memory per container. max 1GB per Container should be sufficient.  

After Part 1 you should be able to start Kafka, make sure it is running, create topics and publish/consume data from kafka with different tools. Feel free to play around with the tools provided and try out different things.
If something is broken beyond repair you can always destroy your environment using `docker-compose down -v` and then start from scratch.  

__Important:__ Whenever it says: Stop here :no_entry: wait for further instructions
## Create Cluster
```sh
# Launch Kafka, Zookeeper, KSQLServer and KafkaProducer
docker-compose up --build -d

# Check if Zookeeper started successfully
# should return 'imok'
echo "echo ruok | nc localhost 2181" | docker exec -i $(docker-compose ps -q zookeeper) /bin/sh -

# Check if Kafka Started succesfully
# should return 'INFO [KafkaServer id=1] started (kafka.server.KafkaServer)'
docker-compose logs kafka | grep started
```

## Create Topics
```sh
# Create a new topic on Kafka
# should return 'Created topic "waterkant".'
# Parameters:
#       - zookeeper: Zookeeper host used for metadata storage
#       - replication-factor: Defines how often each partition is duplicated to prevent dataloss. Since we only have one node, we can not have more then 1 replication
#       - partitions: Defines the paralelism of the topic. This configuration limits how many consumer instances can connect at the same time to the topic.
#       - topic: Name of the topic in kafka
docker-compose exec kafka kafka-topics \
            --create \
            --zookeeper zookeeper:2181 \
            --replication-factor 1 \
            --partitions 3 \
            --topic waterkant
```
Stop here :no_entry:

## Produce Messages
WAIT: Before we continue let us take a look at the `kafkaproducer` code together.
```sh
# Last time we launched the producer it failed right away. Check out the logs of the first run:
docker-compose logs kafkaproducer

# The output should show a message like: 'Unable to produce message: Local: Unknown topic'. This is because our producer started before we created the topic.
# So there was nothing he could publish the messages to. If we restart the docker container it should work smoothly. Run the following command and observe the logs again
docker-compose up --build -d
docker-compose logs -f kafkaproducer
```
Stop here :no_entry:

## Consume messages using kafkacat
```sh
# As you can see in the logs you are succesfully publishing messages to Kafka. But we also want to consume some messages.
# To do that we will make use of a cool utility tool called kafkacat. It will help you maintain kafka clusters in a lot of scenarios.
# Kafkacat is a commandline utility and there is a container with all requirements installed available.
# Let's list all available topics in Kafka for example:
docker run --tty \
           --network waterkant_kafka_default \
           confluentinc/cp-kafkacat \
           kafkacat -b kafka:29092 \
                    -L

# You should see a message like this: 'topic "waterkant" with 3 partitions'
# Check out the number of partitions and on which brokers they reside

# Besides listing available kafka topics we can also produce or consume data with this tool.
# Let's consume our fresh data using kafkacat:
docker run --tty \
           --network waterkant_kafka_default \
           confluentinc/cp-kafkacat \
           kafkacat -b kafka:29092 \
                    -C -t waterkant

# If you want to exit the consumer just hit `CTRL+C`
```
Stop here :no_entry:

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