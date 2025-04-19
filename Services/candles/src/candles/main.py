from loguru import logger
from quixstreams import Application


def run(
    # Kafka parameters
    kafka_broker_address: str,
    kafka_input_input_topic: str,
    kafka_output_topic: str,
    # candles parameters
    candles_sec: int,
):
    """
    Transforms the input stream in candles streams
    in 3 steps
    1- ingest trades from Kafka input topic
    2- aggregate trades into candles
    3- publish candles to Kafka output topic

    Args
    kafka_broker_address -- address of the Kafka broker
    kafka_input_input_topic -- name of the input topic
    kafka_output_topic -- name of the output topic
    Return: None
    """

    app = Application(broker_address=kafka_broker_address)
    # input topic
    trade_topic = app.topic(name=kafka_input_input_topic, value_deserializer='json')
    # output topic
    candle_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # step 1: ingest trade from the input kafka topic
    # create streaming datafram
    sdf = app.dataframe(topic=trade_topic)

    # step 2: aggregate trades into candles
    ## TODO:at the moment we are only printing messages to make sure things work
    sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))

    # step 3: produce the candles to the output kafka topic
    # produce update to the output topic
    sdf = sdf.to_topic(candle_topic)

    # run the streaming application
    app.run()


if __name__ == '__main__':
    run(
        kafka_broker_address='localhost:31234',
        kafka_input_input_topic='trades',
        kafka_output_topic='candles',
        candles_sec=60,
    )
