from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Trader service."""

    model_config = SettingsConfigDict(
        env_file='Services/trader/settings.env', env_file_encoding='utf-8'
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


config = Settings()
# print(config.model_dump())
