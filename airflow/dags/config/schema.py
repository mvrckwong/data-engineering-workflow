from dataclasses import dataclass

@dataclass(frozen=True)
class TelegramBotConfig:
	"""Stores Telegram bot configuration."""
	bot_token: str
	chat_id: str
      
@dataclass(frozen=True)
class CoinAPIConfig:
	"""Stores CoinAPI configuration."""
	api_key: str
	api_url: str

@dataclass(frozen=True)
class AirbyteHTTPConfig:
	"""Stores Airbyte HTTP configuration."""
	airbyte_api_url: str
	airbyte_api_token: str

	airbyte_id: str
	airbyte_host: str
	airbyte_port: int
	airbyte_conn_id: str


if __name__ == "__main__":
    None