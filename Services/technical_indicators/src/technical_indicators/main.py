from datetime import timedelta

import candles
from loguru import logger
from quixstreams import Application

from technical_indicators.config import config



def run(
    # Kafka parameters
    kafka_broker_address: str,
    kafka_input_input_topic: str,
    kafka_output_topic: str,
    # candles parameters
    candles_seconds: int,
    kafka_consumer_group: str,
):
    """
    Transforms the stream of input candles into technical indicators
    in 3 steps
    1- ingest trades from Kafka input topic
    2- aggregate trades into candles
    3- publish candles to Kafka output topic

    Args
    kafka_broker_address -- address of the Kafka broker
    kafka_input_input_topic -- name of the input topic
    kafka_output_topic -- name of the output topic
    candles_seconds -- number of seconds for the candles
    Return: None
    """

    app = Application(broker_address=kafka_broker_address,
                      consumer_group=kafka_consumer_group)
    # input topic
    candles_topic = app.topic(name=kafka_input_input_topic, value_deserializer='json')
    # output topic
    technical_indicators_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # step 1: ingest trade from the input kafka topic for the given candles seconds
    # create streaming datafram
    sdf = app.dataframe(topic=candles_topic)

    # keep only candles with the given candles seconds
    sdf = sdf[sdf['candle_seconds'] == candles_seconds]
    # step 2: computer technical indicators
    ##TODO: add data processing to get technical indicators

    
    #logging to the console
    sdf.update(lambda value: logger.debug(f'Final Message: {value}'))

    # step 3: produce the candles to the output kafka topic
    # produce update to the output topic
    sdf = sdf.to_topic(technical_indicators_topic)

    # run the streaming application
    app.run()

if __name__ == '__main__':
    run(
        kafka_broker_address=config.kafka_broker_address,
        kafka_input_input_topic=config.kafka_input_topic,
        kafka_output_topic=config.kafka_output_topic,
        candles_seconds=config.candles_seconds,
        kafka_consumer_group=config.kafka_consumer_group

    )
