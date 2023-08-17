from . import bot
from telebot import types
import threading
import time
from telebot.util import quick_markup


call_back_query_data = [None]
call_back_query_user = [None]

def gen_markup():
    markup = quick_markup({
        '点击验证':{'callback_data':'verify_click'},
        '由可爱的kiko手动通过':{'callback_data':'admin_verify_click'},
        
    },row_width=2)
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call : types.CallbackQuery):
    call_back_query_data[0] = call.data
    call_back_query_user[0] = call.from_user

def countdown():
    time.sleep(30)

def verify(new_user : types.User):
    if call_back_query_data[0] == 'verify_click' and call_back_query_user[0].username == new_user.username:
        return True
    elif  call_back_query_data[0] == 'admin_verify_click' and call_back_query_user[0].username == 'akiyakiko':
        return True
    

#chat_member_handler. When status changes, telegram gives update. check status from old_chat_member and new_chat_member.
@bot.chat_member_handler()
def chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        
        bot.send_message(message.chat.id, "@{name}你好,请完成验证，否则30秒后将踢出群组".format(new.user.username), reply_markup=gen_markup())
        bot.restrict_chat_member(message.chat.id, new.user.id, until_date=99999999, can_send_messages=False)

        countdownThread = threading.Thread(target=countdown)
        countdownThread.start()
        
        while countdownThread.is_alive():
            result = verify(new.user)
            if result == True:
                bot.restrict_chat_member(message.chat.id, new.user.id, can_send_messages=True)
                bot.send_message(message.chat.id,"@{name}已完成验证，欢迎新成员!".format(name=new.user.username)) # Welcome message
                
                break

            else:
                continue
        if countdownThread.is_alive() == False:
            bot.ban_chat_member(message.chat.id, new.user.id)
            bot.send_message(message.chat.id,"@{name}验证超时，已被ban!".format(new.user.username).format(name=new.user.username))

        


        