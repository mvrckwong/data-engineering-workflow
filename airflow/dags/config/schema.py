from dataclasses import dataclass

# @dataclass(frozen=True)
# class DBConfig:
# 	"""Stores Redshift database connection details."""
# 	host: str
# 	port: int
# 	dbname: str
# 	user: str
# 	password: str

@dataclass(frozen=True)
class TelegramConfig:
	"""Stores Telegram bot configuration."""
	bot_token: str
	chat_id: str


if __name__ == "__main__":
    None