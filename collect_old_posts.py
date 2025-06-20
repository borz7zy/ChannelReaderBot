import asyncio
import random
import config
import csv
import io
from telethon import TelegramClient, errors
from telethon.tl.types import InputMessagesFilterEmpty, MessageService


def contains_ignored_tags(text: str) -> bool:
    lowered = text.lower()
    return any(tag in lowered for tag in config.IGNORE_TAGS)


async def fetch_messages(client, channel):
    messages = []
    async for msg in client.iter_messages(
            channel,
            offset_date=config.MONTH,
            reverse=True,
            limit=None,
            filter=InputMessagesFilterEmpty
    ):
        if isinstance(msg, MessageService):
            continue

        text = msg.message or ""
        if not text.strip() and not msg.media:
            continue
        messages.append(msg)
    return messages


async def main():
    async with TelegramClient(
            session="my_session",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            system_version="4.16.30-vxChannel"
    ) as client:

        all_messages = []

        shuffled_channels = config.CHANNELS[:]
        random.shuffle(shuffled_channels)

        for channel in shuffled_channels:
            clean_channel = channel.strip("@")
            try:
                msgs = await fetch_messages(client, channel)
                print(f"[INFO] Получено сообщений из {channel}: {len(msgs)}")
                for msg in msgs:
                    text = msg.message or ""
                    if contains_ignored_tags(text):
                        continue

                    all_messages.append({
                        "id": msg.id,
                        "channel": clean_channel,
                        "date": msg.date.strftime("%Y-%m-%d %H:%M:%S"),
                        "url": f"https://t.me/{clean_channel}/{msg.id}",
                        "text": text.replace("\n", " ").strip()
                    })
            except Exception as e:
                print(f"[ERROR][{channel}] {e}")

        print(f"[INFO] Всего сообщений к сохранению: {len(all_messages)}")

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "channel", "date", "url", "text"])
        writer.writeheader()
        for item in all_messages:
            writer.writerow(item)

        output.seek(0)

        csv_bytes = io.BytesIO(output.getvalue().encode('utf-8'))
        csv_bytes.name = f"vacancies_{msg.date.strftime("%Y-%m-%d %H:%M:%S")}.csv"

        try:
            await client.send_file(
                config.FORWARD_TO_CHAT,
                file=csv_bytes,
                caption=f"Собрано {len(all_messages)} сообщений",
                reply_to=config.FORWARD_TO_CHAT_TOPIC
            )
            print("[INFO] CSV успешно отправлен.")
        except errors.FloodWaitError as e:
            print(f"[FLOOD_WAIT] Ожидание {e.seconds} секунд...")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"[ERROR] Ошибка при отправке файла: {e}")

        print("Работа завершена.")


if __name__ == "__main__":
    asyncio.run(main())
