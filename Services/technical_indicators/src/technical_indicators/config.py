from ast import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List,Dict
import yaml

class Settings(BaseSettings):
    """Settings for the Trades service."""

    model_config = SettingsConfigDict(
        env_file='Services/technical_indicators/settings.env', env_file_encoding='utf-8')

    kafka_broker_address: str
    kafka_input_topic:str
    kafka_output_topic: str
    candles_seconds: int
    kafka_consumer_group: str
    max_candles_in_state: int
    table_name_in_risingwave: str
    
    

class IndicatorsSettings(BaseSettings):
    """ 
    load technical indicators settings from yaml file
    """
    sma: List[int]
    ema: List[int]
    rsi: List[int]
    macd: Dict[str,int]
    
    # def __init__(self,sma: List[int], ema: List[int], rsi: List[int], macd: List[int]):
    #     self.sma = sma
    #     self.ema = ema
    #     self.rsi = rsi
    #     self.macd = macd
    
    @classmethod
    def from_yaml(cls, file_path: str):
        """
        Load the settings from a yaml file
        """
       
        with open(file_path, 'r') as f:
            config = yaml.safe_load(f)
        indicators =config['technical_indicators']
        return cls(
            sma=indicators['sma'],
            ema=indicators['ema'],
            rsi=indicators['rsi'],
            macd=indicators['macd']
        )

config = Settings()
# print(config.model_dump())
indicator_config = IndicatorsSettings.from_yaml("Services/technical_indicators/src/technical_indicators/config.yaml")

