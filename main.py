import asyncio
import logging
from pathlib import Path

from telethon import TelegramClient

from config import SESSION_NAME, TELEGRAM_API_HASH, TELEGRAM_API_ID
from src.logging import setup_logging

client = TelegramClient(
    Path("sessions", SESSION_NAME),
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
)
logger = logging.getLogger(__name__)


async def main():
    setup_logging(level=logging.INFO)
    logger.info(TELEGRAM_API_ID)


if __name__ == "__main__":
    asyncio.run(main())
