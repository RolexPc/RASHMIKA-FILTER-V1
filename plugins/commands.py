import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import ADMINS, MSG_ALRT, LOG_CHANNEL, PICS, SUPPORT_CHAT_ID
from utils import get_settings, get_size, is_subscribed, save_group_settings, temp
from database.connections_mdb import active_connection
import re
import json
import base64
logger = logging.getLogger(__name__)

BATCH_FILES = {}


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton('⤬ 𝐀ᴅᴅ 𝐌ᴇ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('⤬ 𝐀ᴅᴅ 𝐌ᴇ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ⤬', url=f'http://t.me/{temp.U_NAME}?startchannel=true')        
            ],[
                InlineKeyboardButton('🖥 𝐍𝐄𝐖 𝐎𝐓𝐓 𝐔𝐏𝐃𝐓𝐄𝐒 🖥', url=f'https://t.me/OTT_ARAKAL_THERAVAD_MOVIESS')
            ],
            [
                InlineKeyboardButton('⭕️ 𝐆𝐄𝐓 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊𝐒 ⭕️', url="https://t.me/ARAKAL_THERAVAD_GROUP_LINKS"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('⤬ 𝐀ᴅᴅ 𝐌ᴇ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐆ʀᴏᴜᴘ ⤬', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('⤬ 𝐀ᴅᴅ 𝐌ᴇ 𝐓ᴏ 𝐘ᴏᴜʀ 𝐂𝐡𝐚𝐧𝐧𝐞𝐥 ⤬', url=f'http://t.me/{temp.U_NAME}?startchannel=true')        
            ],[
            InlineKeyboardButton("👥 𝐆𝐑𝐎𝐔𝐏 - 𝟏", url=f"https://t.me/+FPt__pYntKFmODg1"),
            InlineKeyboardButton("𝐆𝐑𝐎𝐔𝐏 - 𝟐 👥", url=f"https://t.me/ARAKAL_THERAVAD_GROUP_02")
            ],[
            InlineKeyboardButton("👥 𝐆𝐑𝐎𝐔𝐏 - 𝟑", url=f"https://t.me/ARAKAL_THERAVAD_GROUP_03"),
            InlineKeyboardButton("𝐆𝐑𝐎𝐔𝐏 - 𝟒 👥", url=f"https://t.me/ARAKAL_THERAVAD_GROUP_04")
            ],[
            InlineKeyboardButton("👥 𝐆𝐑𝐎𝐔𝐏 - 𝟓", url=f"https://t.me/+7CetBQ1fjRU0NTU1"),
            InlineKeyboardButton("𝐆𝐑𝐎𝐔𝐏 - 𝟔 👥", url=f"https://t.me/+1hNd66hCOJM1MTVl")
            ],[
            InlineKeyboardButton("🖥 𝐍𝐄𝐖 𝐎𝐓𝐓 𝐔𝐏𝐃𝐓𝐄𝐒 🖥", url="https://t.me/OTT_ARAKAL_THERAVAD_MOVIESS")
            ],[
            InlineKeyboardButton("🖥 𝐍𝐄𝐖 𝐎𝐓𝐓 𝐈𝐍𝐒𝐓𝐆𝐑𝐀𝐌 🖥", url="https://www.instagram.com/new_ott__updates?igsh=MTMxcmhwamF4eGp6eg==")
            ],[
            InlineKeyboardButton("⭕️ 𝐆𝐄𝐓 𝐎𝐔𝐑 𝐂𝐇𝐀𝐍𝐍𝐄𝐋 𝐋𝐈𝐍𝐊𝐒 ⭕️", url="https://t.me/ARAKAL_THERAVAD_GROUP_LINKS")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)      
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
                                             
