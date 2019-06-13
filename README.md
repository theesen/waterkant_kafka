# Waterkant Festival Workshop - Event Streaming with Kafka
[Waterkant.sh Workshop](https://waterkant19.sched.com/event/POxL/event-streaming-with-kafka)

This repository is created as a guideline for the Kafka event streaming workshop at the Waterkant.sh Festival 2019 in Kiel.
Goal of this workshop is an introduction to Kafka and the possibilities it serves. Since Kafka is a huge tool and has a lot of features we will concentrate on a basic setup and go through several use cases together.

During this workshop we will heavily rely on the Confluent Platform. Confluent is a company that was founded to provide Kafka as a Service. They also open source a lot of their products and contribute to Core Kafka. You can run all of the examples below on bare metal Kafka as well. It is mostly convenience, that we use Confluent Kafka.


# Requirements:
Install Docker: 
* [OS X Installation](https://docs.docker.com/docker-for-mac/)
* [Windows Installation](https://docs.docker.com/docker-for-windows/)
* [Ubuntu Installation](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
* Any other OS users probably know how to do it without me providing some links :)

# Part 1: Launch Kafka
In the first part of our workshop we will launch a fresh Kafka cluster on your local docker environment.
So make sure that you have docker installed and it has sufficient memory per container. (roughly 1GB per Container)  

After Part 1 you should be able to start Kafka, create topics and publish/consume data from Kafka with different tools. Feel free to play around with the tools provided and try out different things.
If something is broken beyond repair you can always destroy your environment using `docker-compose down -v` and then start from scratch.  

__Important:__ Whenever it says: Stop here :no_entry: wait for further instructions.
## Create Cluster
```sh
# Move into the root directory of the project 
# Launch Kafka, Zookeeper, KSQLServer and KafkaProducer using docker-compose
docker-compose up --build -d

# Before we continue, we should check if all required components started successfully.
# Zookeeper is up and running when the 4 letter command 'ruok' returns 'imok'!
echo "echo ruok | nc localhost 2181" | docker exec -i $(docker-compose ps -q zookeeper) /bin/sh -

# For Kafka we will check the kafka logs for a specific messagem, which indicates a healthy started broker.
# The following command should return 'INFO [KafkaServer id=1] started (kafka.server.KafkaServer)'
docker-compose logs kafka | grep started
```

## Create Topics
```sh
# As explained before Kafka is a event streaming system, and events are grouped into topics. 
# Our cluster does not automatically create a topic, so before we can successfully publish data 
# to Kafka, we need to create a topic.
# The following command should return 'Created topic "waterkant".'
# Parameters:
#       - zookeeper: Zookeeper host used for metadata storage
#       - replication-factor: Defines how often each partition is duplicated to prevent dataloss.
#                             Since we only have one node, we can not have more then 1 replication
#       - partitions: Defines the paralelism of the topic. This configuration limits how many 
#                     consumer instances can connect at the same time to the topic.
#       - topic: Name of the topic in Kafka
docker-compose exec kafka kafka-topics \
            --create \
            --zookeeper zookeeper:2181 \
            --replication-factor 1 \
            --partitions 3 \
            --topic waterkant
```
Helpful Links:
* [Confluent Kafka Platform Quickstart Guide](https://docs.confluent.io/current/quickstart/ce-docker-quickstart.html)
* [Kafka Documentation](https://kafka.apache.org/documentation/)
* [Kafka Introduction](https://kafka.apache.org/intro)

Stop here :no_entry:  

## Produce Messages
Before we continue let us take a look at the `kafkaproducer` code together.
```sh
# Last time we launched the producer it failed right away. Check out the logs of the first run:
docker-compose logs kafkaproducer

# The output should show a message like: 'Unable to produce message: Local: Unknown topic'
# at the end.
# This is because our producer started before we created the topic and producing to a topic that does 
# not exist fails if AUTO_CREATE_TOPIC is not enabled. 
# If we restart the docker container it will start producing messages to the topic 'waterkant'
# Run the following command and observe the logs again
docker-compose up --build -d
docker-compose logs -f kafkaproducer
```
Helpful Links:
* [Confluent Kafka Client Library](https://docs.confluent.io/current/clients/index.html)

## Consume messages using kafkacat
```sh
# As you can see in the logs you are succesfully publishing messages to Kafka. But we also want 
# to consume some messages. To do that we will make use of a helpful tool called kafkacat. 

# Kafkacat is a commandline utility tool and there is a container with all requirements installed available.
# Documentation of kafkacat: https://github.com/edenhill/kafkacat
# Kafkacat can list topics, consume data, produce data and show detailed information about topics.
# Let's list all available topics in Kafka:
docker run --tty \
           --network waterkant_kafka_default \
           confluentinc/cp-kafkacat \
           kafkacat -b kafka:29092 \
                    -L

# You should see a message like this: 'topic "waterkant" with 3 partitions'
# Check out the number of partitions and on which brokers they reside

# Besides listing available kafka topics we can also produce or consume data with kafkacat.
docker run --tty \
           --network waterkant_kafka_default \
           confluentinc/cp-kafkacat \
           kafkacat -b kafka:29092 \
                    -C -t waterkant

# If you want to exit the consumer just hit `CTRL+C`
```
Stop here :no_entry:

# Part 2: KSQL 
KSQL is short for Kafka SQL and let's you write regular SQL queries directly on your streaming data inside of Kafka.  
It is possible to join streams, aggregate data from topics and store them in another topic. You can also create compacted tables using Kafka which will always show the most recent version of each key in a topic.
It is pretty much SQL just live and as a stream.
```sh
# KSQL needs a KSQL Server to operate, we launched this one as part of our docker-compose 
# file in the very beginning already. So yours should be up and running.
# You can check this either by running a HTTP request against the KSQL API:
curl -sX GET "http://localhost:8088/info"
# or you can get the logs of the ksql server
docker-compose logs -f ksql-server

# Now we will launch the KSQL cli and run some commands.
docker-compose exec ksql-cli ksql http://ksql-server:8088
# you should be able to see a cli that let's you run commands like this.
# The command will return an empty list. Which is correct since we did not create 
# any ksql streams, and in the ksql terminology streams and topics are different 
# concepts.
show streams;
```
```sql
# Since we know KSQL Server and CLI are up and running it is time to test some SQL.
# First of all we need to create a Stream on top of our Kafka topic. This way KSQL 
# knows the content of the topic and how the data is formated (f.e. Json, Avro, Bytes).
CREATE STREAM waterkantsql 
    (name VARCHAR
     , workshop VARCHAR
     , value INTEGER) 
WITH (KAFKA_TOPIC='waterkant'
    , VALUE_FORMAT='JSON');

# We can check if the stream looks the way we wanted to have it by describing it. 
# This will output some information about system rows (f.e. rowkey) and other settings.
DESCRIBE EXTENDED waterkantsql;

# Now it is time to check out, if there is actually data arriving in our stream. Given that your 
# producer is still up and running you should see data flowing into this stream constantly.
# It might take a few seconds until you see data flowing in. It takes some time for Kafka to register 
# the new stream and consume data from the original topic.
SELECT * FROM waterkantsql;
```
Stop here :no_entry:

```sql
# The last feature we are going to look at is compacted stream, aka tables. 
# Tables are Kafka topic that have a unique key. So whenever a message with the same key is published
# the previous record is being deprecated and consumers only receive the new one. In this example
# we combine compacted streams with a regular count(). This will return the most recent count for each key.
CREATE TABLE waterkant_agg AS
  SELECT rowkey,
         COUNT(*)
  FROM waterkantsql
  GROUP BY rowkey;

SELECT * FROM waterkant_agg;
# You will see the flow of aggregated values in the stream. 
# But it is also possible to filter down to a specific rowkey
SELECT * FROM waterkant_agg where rowkey = 'water';
```

You have learned the basic principles of Kafka and ksql and are free to try out anything that comes to your mind. I recommend trying out different aggregations and other possibilities of KSQL. You can find some hints here:

* [Aggregate Streaming Data](https://docs.confluent.io/current/ksql/docs/developer-guide/aggregate-streaming-data.html)

I would suggest you to generate a new event using the same values for the Kafka key. This way you can try to join two Kafka topics. Either extend the existing python application or use `kafkacat` to manually publish data. Just make sure that you created the new topic beforehand. 
Documentation: 
* [Join Streams in KSQL](https://docs.confluent.io/current/ksql/docs/developer-guide/join-streams-and-tables.html)


#### To infinity and beyond!