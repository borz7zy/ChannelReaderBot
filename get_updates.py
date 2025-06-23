import config
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaStory


client = TelegramClient(
    session=config.ACCOUNT_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    system_version=config.SYSTEM_VERSION
)

CHANNELS = {ch.lower().lstrip('@') for ch in config.CHANNELS}
IGNORE_TAGS = {tag.lower() for tag in config.IGNORE_TAGS}


def contains_ignored_tags(text: str) -> bool:
    text_lower = text.lower()
    return any(tag in text_lower for tag in IGNORE_TAGS)


@client.on(events.NewMessage(incoming=True, outgoing=False))
async def handler(event):
    try:
        if not event.message or not event.message.peer_id:
            return

        sender = await event.get_chat()
        if not sender or not getattr(sender, 'username', None):
            return

        if isinstance(event.message.media, MessageMediaStory):
            return

        sender_username = sender.username.lower()
        if sender_username not in CHANNELS:
            return

        message_text = event.message.message or ""
        if contains_ignored_tags(message_text):
            return

        await client.forward_messages(
            config.FORWARD_TO_CHAT,
            messages=event.message
        )

    except Exception as e:
        print(f"[ERROR] Ошибка обработки сообщения: {e}")


if __name__ == "__main__":
    print("[INFO] Бот запущен. Ожидание сообщений...")
    client.start()
    client.run_until_disconnected()
