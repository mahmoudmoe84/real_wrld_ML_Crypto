from quixstreams import Application
from kraken_api import KrakenAPI , Trade
from typing import Dict, List , Tuple 
from loguru import logger



def run(
    kafka_broker_address: str,
    kafka_topic_name: str,
    kraken_api
):
    app = Application(
        broker_address=kafka_broker_address, 
        consumer_group='example'
    )

# Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name,
                    value_serializer='json')
    with app.get_producer() as producer:
        while True:
            events:list[Trade] = kraken_api.get_trades()

        
            # Create a Producer instance
                # Serialize an event using the defined Topic 
            
            for event in events:
                message = topic.serialize(
                    # key=event["id"],
                    value=event.to_dict())

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name, 
                    value=message.value, 
                    # key=message.key
                )
            logger.info(f'Produced messages to topic {topic.name}')
            # breakpoint()


if __name__ == "__main__":
    api = KrakenAPI(
        product_id=['BTC/EUR']
    )
    
    run(
        kafka_broker_address='localhost:31234',
        kafka_topic_name='trades',
        kraken_api=api
    )