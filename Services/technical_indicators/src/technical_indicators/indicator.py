import numpy as np
from loguru import logger
from talib import stream


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
    indicators['sma_7'] = stream.SMA(close,timeperiod=7)
    indicators['sma_14'] = stream.SMA(close,timeperiod=14)
    indicators['sma_21'] = stream.SMA(close,timeperiod=21)
    indicators['sma_60'] = stream.SMA(close,timeperiod=60)

    #EXPONENTIAL MOVING AVERAGE
    indicators['ema_7'] = stream.EMA(close,timeperiod=7)
    indicators['ema_14'] = stream.EMA(close,timeperiod=14)
    indicators['ema_21'] = stream.EMA(close,timeperiod=21)
    indicators['ema_60'] = stream.EMA(close,timeperiod=60)

    # Realative Strength Index
    indicators['rsi_7'] = stream.RSI(close,timeperiod=7)
    indicators['rsi_14'] = stream.RSI(close,timeperiod=14)
    indicators['rsi_21'] = stream.RSI(close,timeperiod=21)
    indicators['rsi_60'] = stream.RSI(close,timeperiod=60)

    #Moving Average Convergence Divergence
    indicators['macd_7'], indicators['macd_7_signal'], indicators['macd_7_hist'] = stream.MACD(
        close,fastperiod=7,slowperiod=14,signalperiod=9)

    #on balance volume
    indicators['obv'] = stream.OBV(close, volume)
    return {**indicators,**candle} # type: ignore
    # breakpoint()
    # get the candles from the state dictionary
    # candles = state.get(candles_topic)

    # compute the technical indicators from the candlesge
