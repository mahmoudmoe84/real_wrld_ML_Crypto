import numpy as np
from loguru import logger
from talib import stream

from technical_indicators.config import indicator_config


def compute_technical_indicators(
    candle: dict,
    state: dict
) -> None:
    """
    Compute the technical indicators from the candles in the state dictionary
    and publish them to the output topic

    Args
    state -- state dictionary
    candles_seconds -- number of seconds for the candles
    candles_topic -- name of the input topic
    technical_indicators_topic -- name of the output topic
    Return: None
    """

    # Get the candles from the state dictionary
    candles = state.get('candles',default=[])

    logger.debug(f"Number of canles in state: {len(candles)}")

    #extract open,close ,high , low , volume  from the candles
    close = np.array([candle['close'] for candle in candles])
    open = np.array([candle['open'] for candle in candles])
    high = np.array([candle['high'] for candle in candles])
    low = np.array([candle['low'] for candle in candles])
    volume = np.array([candle['volume'] for candle in candles])


    indicators = {}
    # Calculate SMA for different periods
    for period in indicator_config.sma:
        indicators[f'sma_{period}'] = stream.SMA(close, timeperiod=period)


    #EXPONENTIAL MOVING AVERAGE
    for period in indicator_config.ema:
        indicators[f'ema_{period}'] = stream.EMA(close, timeperiod=period)

    # Realative Strength Index
    for period in indicator_config.rsi:
        indicators[f'rsi_{period}'] = stream.RSI(close, timeperiod=period)

    #Moving Average Convergence Divergence
    indicators['macd_7'], indicators['macd_7_signal'], indicators['macd_7_hist'] = stream.MACD(
        close,fastperiod=indicator_config.macd['fastperiod'],
        slowperiod=indicator_config.macd['slowperiod'],
        signalperiod=indicator_config.macd['signalperiod'])

    #on balance volume
    indicators['obv'] = stream.OBV(close, volume)
    return {**indicators,**candle} # type: ignore
    # breakpoint()
    # get the candles from the state dictionary
    # candles = state.get(candles_topic)

    # compute the technical indicators from the candlesge
