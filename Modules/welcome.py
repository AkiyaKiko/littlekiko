from . import bot
from telebot import types

#chat_member_handler. When status changes, telegram gives update. check status from old_chat_member and new_chat_member.
@bot.chat_member_handler()
def chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        bot.send_message(message.chat.id,"欢迎新成员 {name}!".format(name=new.user.first_name)) # Welcome message