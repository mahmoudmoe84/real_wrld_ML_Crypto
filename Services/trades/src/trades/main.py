from typing import Union

from loguru import logger
from quixstreams import Application

from trades.config import config
from trades.kraken_rest_api import KrakenRestAPI
from trades.kraken_websocket_api import KrakenWebsocketAPI, Trade
from trades.trade import Trade


def run(kafka_broker_address: str, kafka_topic_name: str, kraken_api:Union[KrakenWebsocketAPI, KrakenRestAPI]):
    app = Application(broker_address=kafka_broker_address, consumer_group='example')

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic_name, value_serializer='json')
    with app.get_producer() as producer:
        while not kraken_api.is_done():
            events: list[Trade] = kraken_api.get_trades()

            # Create a Producer instance
            # Serialize an event using the defined Topic

            for event in events:
                message = topic.serialize(
                    key=event.product_id,
                    value=event.to_dict()
                )

                # Produce a message into the Kafka topic
                producer.produce(
                    topic=topic.name,
                    value=message.value,
                    key=message.key
                )
                logger.info(f'Produced messages to topic {topic.name}')
                # breakpoint()
                logger.info(f'Trade {event.to_dict()} push to Kafka')


if __name__ == '__main__':
    if config.live_or_historical == 'live':
        logger.info('Creating Krakenwebsockt API object')
        api = KrakenWebsocketAPI(product_id=config.product_id)
    elif config.live_or_historical == 'historical':
        logger.info('Creating KrakenRest API object')
        api = KrakenRestAPI(product_id=config.product_id[0], lant_n_days=30)
    else:
        raise ValueError("Invalid value for live_or_historical. Must be 'live' or 'historical")

    run(
        # kafka_broker_address='localhost:31234',
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic_name=config.kafka_topic_name,
        kraken_api=api,
    )
