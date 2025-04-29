from dataclasses import dataclass

@dataclass(frozen=True)
class TelegramBotConfig:
	"""Stores Telegram bot configuration."""
	token: str
	chat_id: str
      

if __name__ == "__main__":
    None