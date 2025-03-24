import os, logging
import logging.config
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, PORT, WEBHOOK
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from datetime import datetime
from pytz import timezone
from pyrogram.errors import BadRequest, Unauthorized

if WEBHOOK:
    from plugins.web_server import web_server  # Import the function directly
    from aiohttp import web

# Logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=300,
            plugins={"root": "plugins"},
            sleep_threshold=10,
        )
        self.app_runner = None  # Store web server runner

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats        
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = me.mention
        self.username = '@' + me.username
        curr = datetime.now(timezone(TIMEZONE))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')

        # Start the web server for Koyeb health check
        if WEBHOOK:
            app = await web_server()  # Call the function directly
            self.app_runner = web.AppRunner(app)
            await self.app_runner.setup()
            await web.TCPSite(self.app_runner, "0.0.0.0", PORT).start()  # Uses correct PORT

        logging.info(f"{me.first_name} started with Pyrogram v{__version__} (Layer {layer}) on @{me.username}.")

        if LOG_CHANNEL:
            try:
                await self.send_message(
                    LOG_CHANNEL, 
                    text=f"<b>{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!\n\n📅 Dᴀᴛᴇ : <code>{date}</code>\n⏰ Tɪᴍᴇ : <code>{time}</code>\n🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>{TIMEZONE}</code>\n\n🉐 Vᴇʀsɪᴏɴ : <code>v{__version__} (Layer {layer})</code></b>"
                )
            except Unauthorized:             
                LOGGER.warning("Bot isn't able to send message to LOG_CHANNEL")
            except BadRequest as e:
                LOGGER.error(e)

    async def stop(self, *args):
        if self.app_runner:
            await self.app_runner.cleanup()  # Clean up the web server
        await super().stop()
        me = await self.get_me()
        logging.info(f"{me.first_name} is shutting down...")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:                       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

app = Bot()
app.run()
