import json
from typing import Dict

from loguru import logger
from pydantic import BaseModel
from websocket import create_connection


class Trade(BaseModel):
    product_id: str
    price: float
    quantity: float
    timestamp: str

    def to_dict(self) -> Dict:
        return self.model_dump()


class KrakenAPI:
    URL = 'wss://ws.kraken.com/v2'

    def __init__(
        self,
        product_id: list[str],
    ):
        self.product_id = product_id

        # create websocket client
        self._ws_client = create_connection(self.URL)

        # send initial subscribe message to the websocket
        self._subscribe()

    def get_trades(self) -> list[Trade]:
        data: str = self._ws_client.recv()

        if 'heartbeat' in data:
            logger.info('heartbeat received')
            return []
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f'error decoding json: {e}')
            return []
        try:
            trade_data = data['data']
        except KeyError as e:
            logger.error(f'No data field found in the messaga {e}')
            return []

        # trades= []
        # for trade in trade_data:
        #     trades.append(
        #         Trade(
        #             product_id=trade['symbol'],
        #             price=(trade['price']),
        #             quantity=(trade['qty']),
        #             timestamp=trade['timestamp']
        #         )
        #     )
        # using list comprehension
        trades = [
            Trade(
                product_id=trade['symbol'],
                price=float(trade['price']),
                quantity=float(trade['qty']),
                timestamp=trade['timestamp'],
            )
            for trade in trade_data
        ]
        return trades

    def _subscribe(self):
        """
        subscribes to the websocket and waits for the intial snapshot
        and the fiven product_ids
        """
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': self.product_id,
                        'snapshot': False,
                    },
                }
            )
        )
        # discard first two messages as they contain no data
        for _ in self.product_id:
            _ = self._ws_client.recv()
            _ = self._ws_client.recv()

        # breakpoint()
