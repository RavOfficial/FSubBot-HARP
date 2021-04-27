# All credits goes to Adnan for his awesome codes <https://github.com/viperadnan-git/force-subscribe-telegram-bot>
# OfficialBawwa <https://t.me/Official_bawwa>
# @Official_Bawwa

import os
import time
import logging
from config import Config
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

HARP = Client(
   "ForceSub Bot",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)

# get mute request
static_data_filter = filters.create(lambda _, __, query: query.data == "okemuted")

@HARP.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, man):
  user_id = man.from_user.id
  chat_id = man.message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    channel = chat_u
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if lel.message.reply_to_message.from_user.id == user_id:
              lel.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(man.id, text="❗ Join the mentioned 'Channel' and press the 'Unmute Me' button again.🤗", show_alert=True)
      else:
        client.answer_callback_query(man.id, text="❗ You are muted by admins for other reasons.😏", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{lel.from_user.mention} is trying to Unmute himself but I can't unmute him because I am not an admin in this chat.😑")
      else:
        client.answer_callback_query(lel.id, text="❗ Warning: Don't click the button if you can speak freely.👿", show_alert=True)

@HARP.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_u = Config.CHANNEL_USERNAME #channel for force sub
  if chat_u:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator"):
      channel = chat_u
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
         try: #tahukai daala
              chat_u = chat_u.replace('@','')
              tauk = message.from_user.mention
              sent_message = message.reply_text(
                Config.WARN_MESSAGE,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("🗣 Unmute Me", callback_data="okemuted")],
                  [InlineKeyboardButton("🔊 Join Channel", url=f"https://t.me/{chat_u}")]]))
              client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))

         except ChatAdminRequired:
            sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission 😒__")

      except ChatAdminRequired:
         client.send_message(chat_id, text=f"❗ **I am not an admin in {chat_u}**\n__Make me admin in the channel__")

@HARP.on_message(filters.command("start") & ~filters.group & ~filters.channel)
def start(client, message):
   message.reply(Config.START_MESSAGE)


HARP.run()
