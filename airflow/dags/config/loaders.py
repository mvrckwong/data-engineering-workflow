from os import getenv
from dotenv import load_dotenv
from loguru import logger

from .models import TelegramConfig

# def load_redshift_config() -> RedshiftConfig | None:
# 	"""Loads Redshift configuration from environment variables."""
# 	load_dotenv('.env')
# 	host = getenv("REDSHIFT_HOST")
# 	port_str = getenv("REDSHIFT_PORT", "5439")
# 	dbname = getenv("REDSHIFT_DBNAME")
# 	user = getenv("REDSHIFT_USER")
# 	password = getenv("REDSHIFT_PASSWORD")

# 	# Check for missing environment variables
# 	missing = [var for var, val in locals().items() if not val and var != 'port_str' and var != 'missing']
# 	if missing:
# 		logger.error(f"Missing Redshift environment variables: {', '.join(m.upper() for m in missing)}")
# 		return None
      
# 	# Validate variables
# 	try:
# 		port = int(port_str)
# 	except ValueError:
# 		logger.error(f"Invalid REDSHIFT_PORT '{port_str}'. Must be an integer.")
# 		return None

# 	logger.info("Redshift configuration loaded.")
# 	return RedshiftConfig(
# 		host=host, 
#             port=port, 
#             dbname=dbname, 
#             user=user, 
#             password=password
# 	)

def load_telegram_config() -> TelegramConfig | None:
	"""Loads Telegram configuration from environment variables."""
	load_dotenv('.env')
	token = getenv("TELEGRAM_BOT_TOKEN")
	chat_id = getenv("TELEGRAM_CHAT_ID")

	# Check for missing environment variables
	if not token:
		logger.error("Missing or placeholder TELEGRAM_BOT_TOKEN.")
		return None
	if not chat_id:
		logger.error("Missing or placeholder TELEGRAM_CHAT_ID.")
		return None

	logger.info("Telegram configuration loaded.")
	return TelegramConfig(
		bot_token=token, 
		chat_id=chat_id
	)


if __name__ == "__main__":
	None