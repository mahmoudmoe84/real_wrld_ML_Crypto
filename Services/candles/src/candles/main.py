from datetime import timedelta
import time

from loguru import logger
from quixstreams import Application

from candles.config import config
from quixstreams import Application
from quixstreams.models import TimestampType
from typing import Any, Optional, List, Tuple



def custom_ts_extractor(
    value: Any,
    headers: Optional[List[Tuple[str, bytes]]],
    timestamp: float,
    timestamp_type: TimestampType,
) -> int:
    """
    Specifying a custom timestamp extractor to use the timestamp from the message payload 
    instead of Kafka timestamp.
    """
    return value["timestamp_ms"]

def init_candle(trade: dict) -> dict:
    """
    Initialize the candle with first trade
    """
    return {
        'open': trade['price'],
        'high': trade['price'],
        'low': trade['price'],
        'close': trade['price'],
        # 'timestamp_ms': trade['timestamp'],
        'pair': trade['product_id'],
        'volume': trade['quantity'],
    }

def update_candle(candle:dict, trade:dict) -> dict:
    """
    takes the cyrrent candle state and the new trade and updates the candle

    Args
    candle (dict)-- the current candle state
    trade (dict) -- the new trade
    Return
        Dict: the updated candle
    """

    # update open price if it is the first message
    # update high and low prices
    candle['high'] = max(candle['high'], trade['price'])
    candle['low'] = min(candle['low'], trade['price'])
    # update close price
    candle['close'] = trade['price']

    # update volume and count
    candle['volume'] += trade['quantity']
    return candle


def run(
    # Kafka parameters
    kafka_broker_address: str,
    kafka_input_input_topic: str,
    kafka_output_topic: str,
    # candles parameters
    candles_seconds: int,
    kafka_consumer_group: str,
    emit_intermediate_candle: bool = True,
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
    candles_seconds -- number of seconds for the candles
    Return: None
    """

    app = Application(broker_address=kafka_broker_address,
                      consumer_group=kafka_consumer_group)
    # input topic
    trade_topic = app.topic(name=kafka_input_input_topic, value_deserializer='json',timestamp_extractor=custom_ts_extractor)
    # output topic
    candle_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    # step 1: ingest trade from the input kafka topic
    # create streaming datafram
    sdf = app.dataframe(topic=trade_topic)

    # step 2: aggregate trades into candles
    ## TODO:at the moment we are only printing messages to make sure things work
    # sdf = sdf.update(lambda message: logger.info(f'Input: {message}'))

    sdf = (
        sdf.tumbling_window(timedelta(seconds=candles_seconds),grace_ms=86400000*30)
        .reduce(reducer=update_candle, initializer=init_candle)
    )
    # if emit_intermediate_candle:
        # emit intermediate candles to make system more responsive
    sdf = sdf.current()
    # else:
    #     # emit only final candles
    #     sdf =sdf.final()

    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    # sdf['timestamp_ms'] = sdf['timestamp']
    sdf['pair'] = sdf['value']['pair']
    sdf['volume'] = sdf['value']['volume']

    #extract window stafrt and end
    sdf['window_start_ms'] = sdf['start']
    sdf['window_end_ms'] = sdf['end']

    #keep only relevant columns
    sdf =sdf[['pair', 'open', 'high', 'low', 'close', 'volume', 'window_start_ms', 'window_end_ms']]

    sdf['candle_seconds'] = candles_seconds
    #logging to the console
    sdf.update(lambda value: logger.debug(f'Candle: {value}'))

    # step 3: produce the candles to the output kafka topic
    # produce update to the output topic
    sdf = sdf.to_topic(candle_topic)

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
