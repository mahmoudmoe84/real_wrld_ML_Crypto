import datetime
from typing import Dict

from pydantic import BaseModel


class Trade(BaseModel):
    product_id: str
    price: float
    quantity: float
    timestamp: str
    timestamp_ms:int


    def to_dict(self) -> Dict:
        return self.model_dump()
    
    @staticmethod
    def iso_format_to_unix_seconds(timestamp: str) -> float:
        """Convert a timestamp in ISO format to seconds.

        Args:
            timestamp (str): _description_

        Returns:
            float: _description_
        """
        return datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp()
    
    @staticmethod
    def unix_seconds_to_iso_format(timestamp_sec: float) -> str:
        """Convert a timestamp in seconds to ISO format.

        Args:
            timestamp_sec (float): _description_

        Returns:
            str: _description_
        """
        dt = datetime.datetime.fromtimestamp(timestamp_sec, tz=datetime.timezone.utc)
        return dt.isoformat().replace("+00:00", "Z")

    @classmethod
    def from_kraken_websocket_response(cls,
                                 product_id:str,
                                 quantity:float,
                                 price:float,
                                 timestamp:str)-> 'Trade':
        """create a Trade object from the Kraken WebSocket response.

        Args:
            product_id (str): _description_
            quantity (float): _description_
            price (float): _description_
            timestamp:str): timestamp in ISO format
        """
        
        return cls(
            product_id=product_id,
            quantity=quantity,
            price=price,
            timestamp=timestamp,
            timestamp_ms=int(cls.iso_format_to_unix_seconds(timestamp)*1000)
        )
    
    @classmethod
    def from_kraken_api_response(cls,
                                 product_id:str,
                                 quantity:float,
                                 price:float,
                                 timestamp_sec:float)-> 'Trade':
        """create a Trade object from the Kraken API response.

        Args:
            product_id (str): _description_
            quantity (float): _description_
            price (float): _description_
            timestamp_sec (float): _description_
        """
        return cls(
            product_id=product_id,
            quantity=quantity,
            price=price,
            timestamp=cls.unix_seconds_to_iso_format(timestamp_sec),
            timestamp_ms=int(timestamp_sec * 1000)
        )
