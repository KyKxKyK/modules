
#

#              © Copyright 2022

#

#          https://t.me/kyk_kyk

#

# 🔒 Licensed under the GNU GPLv3

# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @kyk_kyk

from .. import loader, utils

from telethon.tl.types import Message

import logging

import asyncio

from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

from telethon.errors.rpcerrorlist import BotResponseTimeoutError

logger = logging.getLogger(__name__)

@loader.tds

class DeleteAccountMod(loader.Module):

    """Clicker"""

    strings = {"name": "DeleteAccount"}

    _chat = 1543388590

    _request_timeout = 4

    async def client_ready(self, client, db):

        self._db = db

        self._client = client

        self._tg_id = (await client.get_me()).id

    async def delacccmd(self, message: Message):

        """Для удаления аккаунта"""

        first_start = True

        self._db.set(self.strings["name"], "state", True)

        

        while self._db.get(self.strings["name"], "state", False):

            if first_start:

                await message.edit("👩‍💼 <b>Жди</b>")

            for text in {"Мой генератор [AFK]", "Мой бизнес [AFK]", "Моя ферма [AFK]"}:

                await self._client.send_message(self._chat, text)

                await asyncio.sleep(3)

            if first_start:

                await message.edit("🚽 <b>Жду ответ бота...</b>")

            await asyncio.sleep(6)

            if first_start:

                await message.edit("🔎 <b>Ищу сообщения с кнопками...</b>")

            

            messages = {}

            async for msg in self._client.iter_messages(self._chat, limit=50):

                if not getattr(msg, "reply_markup", False):

                    continue

                try:

                    data = msg.reply_markup.rows[0].buttons[1].data

                except (AttributeError, IndexError):

                    continue

                logger.info(data)

                if data == b"payTaxesGenerator":

                    messages["generator"] = msg

                elif data == b"payTaxesFarm":

                    messages["farm"] = msg

                elif data == b"payTaxes":

                    messages["business"] = msg

                found_all = True

                for i in {"farm", "business", "generator"}:

                    if i not in messages:

                        found_all = False

                        break

                if found_all:

                    break

            if first_start:

                for i in {"farm", "business", "generator"}:

                    if i not in messages:

                        await message.edit("🚫 <b>Не могу найти сообщения</b>")

                        return

            if first_start:

                messages_formatted = (

                    f"<b>Генератор</b>: <a href=\"https://t.me/c/{self._chat}/{messages['generator'].id}\">#{messages['generator'].id}</a>\n"

                    f"<b>Ферма</b>: <a href=\"https://t.me/c/{self._chat}/{messages['farm'].id}\">#{messages['farm'].id}</a>\n"

                    f"<b>Бизнес</b>: <a href=\"https://t.me/c/{self._chat}/{messages['business'].id}\">#{messages['business'].id}</a>\n\n"

                )

                await message.edit("✅ <b>Готово.</b>\n<i>Запускаю афк режим...</i>")

                await self.inline.form(

                    message=utils.get_chat_id(message),

                    text=f"🍏 <b>Блять , вроде работает. Аминь нахуй чтобы не сломалось...Кук лучший</b>\n\n{messages_formatted}",

                    reply_markup=[[{"text": "🚨 Удалить мой аккаунт", "data": "kykfarmstop"}]],

                )

            async def click(message_id: int, data: bytes):

                try:

                    await self._client(

                        GetBotCallbackAnswerRequest(

                            self._chat,

                            message_id,

                            data=data,

                        )

                    )

                except BotResponseTimeoutError:

                    pass  # Ignore error bc bot doesn't answer callback query

                return True

            for message_id, data in [

                (messages["generator"].id, b"payTaxesGenerator"),

                (messages["business"].id, b"payTaxes"),

                (messages["farm"].id, b"payTaxesFarm"),

            ]:

                if not await click(message_id, data):

                    return

                await asyncio.sleep(self._request_timeout)

            first_start = False

            await asyncio.sleep(60 * 60)

    async def kyk_callback_handler(self, call: "InlineCall"):  # noqa: F821

        if call.data != "kykfarmstop" or call.from_user.id not in [self._tg_id]:

            return

        self._db.set(self.strings["name"], "state", False)

        await call.answer("Остановлено!")

        await getattr(self.inline, "bot", self.inline._bot).edit_message_text(

            inline_message_id=call.inline_message_id,

            text="🚨 <b>Остановлено</b>",

            parse_mode="HTML",

        )
