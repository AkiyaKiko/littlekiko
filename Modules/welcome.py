from . import bot
from telebot import types
import threading
import time
from telebot.util import quick_markup


call_back_query_data = [None]
call_back_query_user = [None]
Running = True
timeout = False

#generate inline keyboard
def gen_markup():
    markup = quick_markup({
        '点击验证':{'callback_data':'verify_click'},
        '由可爱的kiko手动通过':{'callback_data':'admin_verify_click'},
        
    },row_width=2)
    return markup

#handle callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call : types.CallbackQuery):
    call_back_query_data[0] = call.data
    call_back_query_user[0] = call.from_user

#verification countdown
def countdown():
    for count in range(0,30):
        global Running
        global timeout
        if Running == False:
            break
        elif Running == True and timeout == False:
            time.sleep(1)
        elif Running == True and count == 29:
            timeout = True
#initialize Running and timeout
def countdown_init():
    global Running,timeout
    Running = True
    timeout = False

#initialize the callback data and user
def callback_init():
    global call_back_query_data,call_back_query_user
    call_back_query_data = [None]
    call_back_query_user = [None]
        
#verify the click callback
def verify(new_user : types.User):
    if call_back_query_data[0] == 'verify_click' and call_back_query_user[0].username == new_user.username:
        return True
    elif  call_back_query_data[0] == 'admin_verify_click' and call_back_query_user[0].username == 'akiyakiko':
        return True
    

#chat_member_handler. When status changes, telegram gives update. check status from old_chat_member and new_chat_member.
@bot.chat_member_handler()
def chat_m(message: types.ChatMemberUpdated):
    global Running
    global timeout
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":
        
        bot.send_message(message.chat.id, "@{name}你好,请完成验证，否则30秒后将踢出群组".format(new.user.username), reply_markup=gen_markup())
        bot.restrict_chat_member(message.chat.id, new.user.id, until_date=99999999, can_send_messages=False)

        #Countdown_thread
        countdownThread = threading.Thread(target=countdown)
        countdownThread.start()
        
        #Verification_complete
        while countdownThread.is_alive():
            result = verify(new.user)
            if result == True:
                bot.restrict_chat_member(message.chat.id, new.user.id, can_send_messages=True)
                bot.send_message(message.chat.id,"@{name}已完成验证，欢迎新成员!".format(name=new.user.username)) # Welcome message
                Running = False
                callback_init() #verification completed, initialize callback
                break

            else:
                continue

        #Timeout Ban
        if timeout == True:
            bot.ban_chat_member(message.chat.id, new.user.id)
            bot.send_message(message.chat.id,"@{name}验证超时，已被ban!".format(new.user.username).format(name=new.user.username))
        
        #final_initial
        if not countdownThread.is_alive():
            countdown_init()
                

        


        