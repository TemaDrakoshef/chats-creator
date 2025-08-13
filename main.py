import asyncio
import logging
from pathlib import Path

from telethon import TelegramClient

from config import SESSION_NAME, TELEGRAM_API_HASH, TELEGRAM_API_ID
from src.logging import setup_logging
from src.telegram import create_chat, send_message_to_chat

client = TelegramClient(
    Path("sessions", SESSION_NAME),
    api_id=TELEGRAM_API_ID,
    api_hash=TELEGRAM_API_HASH,
)
logger = logging.getLogger(__name__)


async def main():
    setup_logging(level=logging.INFO)
    try:
        await client.start()
        me = await client.get_me()
    except Exception as e:
        logger.critical("Критическая ошибка при подключении бота: %s", e)
        logger.info("Проверьте TELEGRAM_API_HASH, TELEGRAM_API_ID")
        return
    else:
        logger.info("%s: Софт успешно подключился к аккаунту", me.phone)

    chat_title = "My chat"
    chat_about = "This is my chat"
    new_chat = await create_chat(client, chat_title, chat_about)

    if new_chat:
        message_content = "Привет всем!"
        await send_message_to_chat(client, new_chat, message_content)
    else:
        logger.info(
            "%s: Пропуск отправки сообщения, так как создание чата не удалось",
            me.phone,
        )

    logger.info("%s: Завершение работы", me.phone)


if __name__ == "__main__":
    asyncio.run(main())
