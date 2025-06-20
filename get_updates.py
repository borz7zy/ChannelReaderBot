import config
from telethon import TelegramClient, events


client = TelegramClient(
    session="my_session",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    system_version="4.16.30-vxChannel"
)

CHANNELS = {ch.lower().lstrip('@') for ch in config.CHANNELS}
IGNORE_TAGS = {tag.lower() for tag in config.IGNORE_TAGS}


def contains_ignored_tags(text: str) -> bool:
    text_lower = text.lower()
    return any(tag in text_lower for tag in IGNORE_TAGS)


@client.on(events.NewMessage())
async def handler(event):
    try:
        if not event.message or not event.message.peer_id:
            return

        sender = await event.get_chat()
        if not sender or not getattr(sender, 'username', None):
            return

        sender_username = sender.username.lower()
        if sender_username not in CHANNELS:
            return

        message_text = event.message.message or ""
        if contains_ignored_tags(message_text):
            return

        await client.send_message(
            config.FORWARD_TO_CHAT,
            message=event.message,
            reply_to=config.FORWARD_TO_CHAT_TOPIC
        )

    except Exception as e:
        print(f"[ERROR] Ошибка обработки сообщения: {e}")


async def main():
    print("[INFO] Бот запущен. Ожидание сообщений...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    client.loop.run_until_complete(main())
