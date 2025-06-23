from datetime import datetime, timedelta, timezone
import os


"""
Unix:
export TELEGRAM_API_ID="123456"
export TELEGRAM_API_HASH="jntjhbve71nt57131rjf392fg2"
export TELEGRAM_ACCOUNT_NAME="MyAccount"

Windows PowerShell:
$Env:TELEGRAM_API_ID = "123456"
$Env:TELEGRAM_API_HASH = "jntjhbve71nt57131rjf392fg2"
$Env:TELEGRAM_ACCOUNT_NAME = "MyAccount"

Windows CMD.exe:
set TELEGRAM_API_ID=123456
set TELEGRAM_API_HASH=jntjhbve71nt57131rjf392fg2
set TELEGRAM_ACCOUNT_NAME=MyAccount
"""
API_ID = os.getenv("TELEGRAM_API_ID")  # api_id из my.telegram.org/apps
API_HASH = os.getenv("TELEGRAM_API_HASH")  # api_hash из my.telegram.org/apps
ACCOUNT_NAME = os.getenv("TELEGRAM_ACCOUNT_NAME", "my_session")  # указать название сессии

SYSTEM_VERSION = os.getenv("TELEGRAM_SYSTEM_VERSION", "4.16.30-vxChannel")  # версия приложения, если будет выкидывать
                                                                            # из сессии - поменять

CHANNELS = [

]  # Здесь указать список каналов, которые нужно слушать. Пример: "@ChannelOne", "@ChannelTwo", "@ChannelThree"
IGNORE_TAGS = {

}  # Здесь указать список слов по которым посты будут игнорироваться, например: "Junior", "#resume", "#mytag"

MONTH = datetime.now(timezone.utc) - timedelta(days=30)  # Период для сбора через collect_old_posts.py
# (сейчас последние 30 дней)

FORWARD_TO_CHAT = 1  # ID чата, в который требуется отправить файл с собранными вакансиями
