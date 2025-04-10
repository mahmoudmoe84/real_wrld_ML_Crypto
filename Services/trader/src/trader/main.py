import time
from quixstreams import Application


app = Application(
    broker_address='localhost:31234', consumer_group='example'
)

# Define a topic "my_topic" with JSON serialization
topic = app.topic(name='my_topic', value_serializer='json')



while True:
    event = {"id": "1", "text": "Lorem ipsum dolor sit amet"}

    # Create a Producer instance
    with app.get_producer() as producer:

        # Serialize an event using the defined Topic 
        message = topic.serialize(key=event["id"], value=event)

        # Produce a message into the Kafka topic
        producer.produce(
            topic=topic.name, value=message.value, key=message.key
        )
        
        time.sleep(1)