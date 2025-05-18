# from wsgiref import headers
import trades
from trades.trade import Trade
import time 
import requests
from loguru import logger
import json


class KrakenRestAPI:
    
    URL  = 'https://api.kraken.com/0/public/Trades'
    
    def __init__(self,product_id:str,
                 lant_n_days:int):
        self.product_id = product_id
        self.lant_n_days = lant_n_days
        self._is_done = False

        #convert to nanosecodns
        self.since_timestamp_ns = int(
            
            time.time_ns() - (lant_n_days * 24 * 60 * 60 * 1_000_000_000))
        
    
    def get_trades(self) -> list[Trade]:
        """sends a GET request to the Kraken API and returns a list of trades for given product_id 
        and since time given in timestamp in nanoseconds.

        Returns:
            list[Trade]: List of trades for the given product_id and since the given timestamp
        """
        headers = {'Accept': 'application/json'}
        params = {
            'pair': self.product_id,
            'since': self.since_timestamp_ns
        }
        try:
            #send get request to the Kraken API
            response = requests.request('GET',self.URL, headers=headers, params=params)
        except requests.exceptions.SSLError as e:
            logger.error(f"Kraken API is not reachable Error: {e}")
            #wait for 10 seconds before retrying
            # it would be better to make this source statful and recoverable
            # the container gets down and self restarts by kubernetes
            #it can resume from where it left off
            logger.error("Waiting for 10 seconds before retrying...")
            time.sleep(10)
            return []
        
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to deconde / parse data as json: {e}")
            return []
        try:
            #get trades
            trades = data['result'][self.product_id]
        except KeyError as e:
            logger.error(f"Faild to get trades for pairs {self.product_id}: {e}")
            return []
        
        # transform the trades to Trade objects
        trades = [
            Trade.from_kraken_api_response(
                product_id=self.product_id,
                quantity=float(trade[1]),
                price=float(trade[0]),
                timestamp_sec=float(trade[2])
            )
            for trade in trades
        ]
        # breakpoint()  
        
        #update the since timestamp to the last trade timestamp
        self.since_timestamp_ns = int(float(data['result']['last']))
        
        #check stopping condition
        if self.since_timestamp_ns > int(time.time_ns()-1_000_000_000):
            # if the since timestamp is greater than the current time, stop the API call
            # this means that there are no more trades to be fetched
            # and the API call is not needed anymore
            # this is a stopping condition
            # it would be better to make this source statful and recoverable
            # the container gets down and self restarts by kubernetes
            # it can resume from where it left off  
            self._is_done = True
        return trades
    
    def is_done(self) -> bool:
        """returns True if the API call is done and no more trades are to be fetched"""
        return self._is_done