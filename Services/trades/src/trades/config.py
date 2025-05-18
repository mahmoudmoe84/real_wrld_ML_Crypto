from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Trades service."""

    model_config = SettingsConfigDict(
        env_file='Services/trades/settings.env', env_file_encoding='utf-8'
    )
    product_id: list[str] = [
        'BTC/EUR',
        'BTC/USD',
        'ETH/EUR',
        'ETH/USD',
        'SOL/EUR',
        'SOL/USD',
        'XRP/EUR',
        'XRP/USD',
    ]
    kafka_broker_address: str
    kafka_topic_name: str
    live_or_historical: Literal['live', 'historical'] = 'live'
    last_n_days: int = 30

config = Settings()
# print(config.model_dump())
