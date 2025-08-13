import logging

from telethon import TelegramClient, functions, types

logger = logging.getLogger(__name__)


async def create_chat(client: TelegramClient, title: str, about: str):
    """
    Создает новый приватный чат.

    :param client_obj: Экземпляр TelegramClient.
    :param chat_title: Название нового чата.
    :return: Объект сущности созданного чата (Channel) или None в случае ошибки.
    """
    me = await client.get_me()
    logger.info("%s: Попытка создать чат с названием: '%s'", me.phone, title)

    try:
        result = await client(
            functions.channels.CreateChannelRequest(
                title=title, about=about, megagroup=True
            )
        )

        created_channel_entity = None
        if isinstance(result, types.Updates):
            for chat_obj in result.chats:
                if isinstance(chat_obj, types.Channel):
                    created_channel_entity = chat_obj
                    break

        if created_channel_entity:
            logger.info(
                "%s: Чат '%s' успешно создан. ID: '%s'",
                me.phone,
                title,
                created_channel_entity.id,
            )
            return created_channel_entity
        else:
            logger.error(
                "%s: Не удалось найти созданный чат '%s' в ответе API",
                me.phone,
                title,
            )
            return None
    except Exception as e:
        logger.error(
            "%s: Непредвиденная ошибка при создании чата: %s",
            me.phone,
            e,
        )
        return None


async def send_message_to_chat(
    client: TelegramClient, chat_entity: types.Chat, message_text: str
):
    """
    Отправляет текстовое сообщение в указанный чат.

    :param client: Экземпляр TelegramClient.
    :param chat_entity: Сущность чата (Channel), куда будет отправлено сообщение.
    :param message_text: Текст сообщения для отправки.
    :return: Отправленное сообщение (custom.Message) или None в случае ошибки.
    """
    me = await client.get_me()
    logger.info(
        "%s: Отправка сообщения в чат '%s'...", me.phone, chat_entity.title
    )

    try:
        sent_message = await client.send_message(chat_entity, message_text)
        logger.info(
            "%s: Сообщение успешно отправлено в чат '%s'",
            me.phone,
            chat_entity.title,
        )
        return sent_message
    except Exception as e:
        logger.error(
            "%s: Непредвиденная ошибка при отправке сообщения в чат '%s': %s",
            me.phone,
            chat_entity.title,
            e,
        )
        return None
