
# import candles
from loguru import logger
from quixstreams import Application

from technical_indicators.candle import update_candles_in_state
from technical_indicators.config import config
from technical_indicators.indicator import compute_technical_indicators


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

    # Step 2: Filter the candles by the given candles seconds
    sdf =sdf[sdf['candle_seconds'] == candles_seconds]
    # keep only candles with the given candles seconds

    # step 3: Add candles to the state dictionary
    ##TODO:

    # Apply a custom function and inform StreamingDataFrame
    # to provide a State instance to it using "stateful=True"
    sdf = sdf.apply(update_candles_in_state, stateful=True)

    # sdf = sdf.update(lambda value: logger.debug(f'Updated candle: {value}'))
    # sdf = sdf.update(lambda _: breakpoint())
    # Step 4 : compute the technical indicators from the candles in the state dictionary

    sdf = sdf.apply(compute_technical_indicators, stateful=True)

    #logging to the console
    sdf = sdf.update(lambda value: logger.debug(f'Final Message: {value}'))

    # step 5: produce the candles to the output kafka topic
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
