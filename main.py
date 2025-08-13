import asyncio
from pathlib import Path

from telethon import TelegramClient

from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, SESSION_NAME


client = TelegramClient(
    Path("sessions", SESSION_NAME),
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
)


async def main():
    print(TELEGRAM_API_ID)


if __name__ == "__main__":
    asyncio.run(main())
