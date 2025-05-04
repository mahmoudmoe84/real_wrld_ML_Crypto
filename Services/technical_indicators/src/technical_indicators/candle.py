from quixstreams import State

from .config import config


def are_same_window(candle:dict, previous_candle:dict) -> bool:
    """
    returns True if the two candles are in the same window ands crypt currency, False otherwise.
    Args:
        candle (dict): The first candle.
        previous_candle (dict): The second candle.

    Returns:
        bool: True if the candles are in the same window, False otherwise.
    """
    return (
        candle['pair'] == previous_candle['pair']
        and candle['window_start_ms'] == previous_candle['window_start_ms']
        and candle['window_end_ms'] == previous_candle['window_end_ms']
    )

def update_candles_in_state(candle: dict, state: State):
    """_summary_
    This function takes the candle current state (with the list N of previous candles) and the latest candle
    and uppdates the list
    
    it can either happen  that the latest candle corresponds to the same window as the last candle in the state
    or it can be a new candle that corresponds to a new window

    Args:
        candle (dict): latest candle
        state (State): current state of the candles
    Returns:
        None
    """
    candles = state.get('candles', default=[])
    # we need to check if the new candles crosponds to the same (window_start_ms,window_end_ms) as candles[-1]
    if not candles:
        # if the state is empty, we add the new candle to the state
        candles.append(candle)
    elif  are_same_window(candle,candles[-1]):
        #replace the last candle in state
        candles[-1] = candle
    else:

        # add the new candle to the state
        candles.append(candle)

    if len(candles) >config.max_candles_in_state:
        # remove the oldest candle
        candles.pop(0)

    state.set('candles', candles)
    return candle
    # total += 1
    # state.set('total', total)
    # return {**candle, 'total': total}
