import asyncio
import logging
import os
import random
from pathlib import Path

from telethon import TelegramClient

from config import (
    CHAT_ABOUT,
    CHAT_TITLE,
    MAX_SLEEP_CHATS,
    MAX_SLEEP_MESSAGE,
    MESSAGES,
    MIN_SLEEP_CHATS,
    MIN_SLEEP_MESSAGE,
    TELEGRAM_API_HASH,
    TELEGRAM_API_ID,
    TOTAL_CHATS,
)
from src.load_accounts import load_tdata
from src.logging import setup_logging
from src.telegram import create_chat, send_message_to_chat

logger = logging.getLogger(__name__)


def check_folders(folders: list[str]):
    """
    Проверяет наличие папок и создает их, если они отсутствуют.

    Args:
        folders (list[str]): Список путей к папкам для проверки.
    """
    for folder in folders:
        if Path(folder).exists():
            continue
        Path(folder).mkdir()


async def main():
    setup_logging(level=logging.INFO)
    check_folders(folders=["feed_tdata", "sessions"])

    if os.listdir("feed_tdata"):
        await load_tdata()
    sessions = os.listdir("sessions")
    if not os.listdir("sessions"):
        logger.error("Не найдено ни одной сессии в папке 'sessions'")
        return

    for session in sessions:
        client = TelegramClient(
            Path("sessions", session),
            api_id=TELEGRAM_API_ID,
            api_hash=TELEGRAM_API_HASH,
        )

        try:
            await client.start()
            me = await client.get_me()
        except Exception as e:
            logger.critical("Критическая ошибка при подключении бота: %s", e)
            logger.info("Проверьте TELEGRAM_API_HASH, TELEGRAM_API_ID")
            return
        else:
            logger.info("%s: Софт успешно подключился к аккаунту", me.phone)

        chats_created = 0
        for _ in range(TOTAL_CHATS):
            await asyncio.sleep(
                random.randint(MIN_SLEEP_CHATS, MAX_SLEEP_CHATS)
            )
            new_chat = await create_chat(client, CHAT_TITLE, CHAT_ABOUT)
            if new_chat:
                chats_created += 1
                for message_content in MESSAGES:
                    await send_message_to_chat(
                        client, new_chat, message_content
                    )
                    await asyncio.sleep(
                        random.randint(MIN_SLEEP_MESSAGE, MAX_SLEEP_MESSAGE)
                    )
            else:
                logger.info(
                    "%s: Пропуск отправки сообщения, так как создание чата не удалось",
                    me.phone,
                )
        logger.info(
            "%s: Завершение работы. Создано %d чатов", me.phone, chats_created
        )


if __name__ == "__main__":
    asyncio.run(main())
