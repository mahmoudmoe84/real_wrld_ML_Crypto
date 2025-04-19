from kraken_api import KrakenAPI, Trade
from loguru import logger
from quixstreams import Application

from trader.config import config


def run(kafka_broker_address: str, kafka_topic_name: str, kraken_api):
    app = Application(broker_address=kafka_broker_address, consumer_group='example')

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')
    with app.get_producer() as producer:
        while True:
            events: list[Trade] = kraken_api.get_trades()

            # Create a Producer instance
            # Serialize an event using the defined Topic

            for event in events:
                message = topic.serialize(
                    # key=event["id"],
                    value=event.to_dict()
                )

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    # key=message.key
                )
                logger.info(f'Produced messages to topic {topic.name}')
                # breakpoint()
                logger.info(f'Trade {event.to_dict()} push to Kafka')


if __name__ == '__main__':
    api = KrakenAPI(product_id=config.product_id)
    run(
        # kafka_broker_address='localhost:31234',
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        kraken_api=api,
    )
