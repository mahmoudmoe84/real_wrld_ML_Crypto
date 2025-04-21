from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Trades service."""

    model_config = SettingsConfigDict(
        env_file='Services/candles/settings.env', env_file_encoding='utf-8')

    kafka_broker_address: str
    kafka_input_topic:str
    kafka_output_topic: str
    candles_seconds: int
    kafka_consumer_group: str


config = Settings()
# print(config.model_dump())
