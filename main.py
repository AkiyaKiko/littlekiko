import telebot
import threading
import time
import logging
from telebot import util
from telebot import types
from Modules import autoPicture as ap
from telebot.util import quick_markup


# from telebot import apihelper
# apihelper.proxy = {'http':'http://127.0.0.1:10809'}




################################################initialization#################################################
bot = telebot.TeleBot("TOKEN")
#welcome
call_back_query_data = [None]
call_back_query_user = [None]
Running = True
timeout = False

################################################command########################################################
@bot.message_handler(commands=['start','help'])
def send_welcome(message : types.Message):
    bot.reply_to(message, "你好！我是littlekiko！我的主人是https://t.me/akiyakiko")
    bot.send_message(message.chat.id, "可以对我使用指令：\n /git --- 查看我的GitHub仓库\n /图 --- 获取一份随机图片\n /色图 --- 获取一份随机色图\n /透 --- 回复你要透的对象就能自动透了\n")
    

#tou!
@bot.message_handler(commands=['透', '内射', '干烂'])
def tou(message : types.Message):
    command = message.text.replace('/','')
    bot.reply_to(message,'{} {}了 {}'.format(message.from_user.first_name, command, message.reply_to_message.from_user.first_name))

#picture
@bot.message_handler(commands=['图'])
def send_picture(message : types.Message):
    url = 'https://api.nyan.xyz/httpapi/sexphoto'
    params = {'num': '1', 'r18': 'false'}
    bot.reply_to(message, ap.getAutoPicture(url,params))

#ero_picture
@bot.message_handler(commands=['色图'])
def send_ero_picture(message : types.Message):
    url = 'https://api.nyan.xyz/httpapi/sexphoto'
    params = {'num': '1', 'r18': 'true'}
    bot.reply_to(message, ap.getAutoPicture(url, params))

@bot.message_handler(commands=['git'])
def send_git_repo(message : types.Message):
    git_repository = 'https://github.com/AkiyaKiko/littlekiko'
    bot.reply_to(message, git_repository)

################################################keyword########################################################
#sese rebot !! seigo    
@bot.message_handler(regexp='色色')
def repeat_reply(message):
    #group sese
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        bot.reply_to(message, '色色！')
    #pm sese
    if message.chat.type == 'private':
        bot.reply_to(message, '啊哈！虽然是私聊，但还是不能对我单独色色哦！')

#good night
@bot.message_handler(regexp='晚安')
def haveAGoodnight(message):
    bot.reply_to(message, '晚安！')

#Subscription
@bot.message_handler(regexp='订阅')
def supportSub(message):
    bot.reply_to(message, '啊哈，以下是免费的订阅链接哦：https://sub.sharecentre.online/sub 公益链接提供者：@ShareCentrePro')

################################################welcome########################################################
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

        bot.send_message(message.chat.id,"Hello {name}!".format(name=new.user.first_name)) # Welcome message
        bot.send_message(message.chat.id, "@{}你好,请完成验证，否则30秒后将踢出群组".format(new.user.username), reply_markup=gen_markup())
        bot.restrict_chat_member(message.chat.id, new.user.id, until_date=99999999, can_send_messages=False)

        #Countdown_thread
        countdownThread = threading.Thread(target=countdown)
        countdownThread.start()
        
        #Verification_complete
        while countdownThread.is_alive():
            result = verify(new.user)
            if result == True:
                bot.restrict_chat_member(message.chat.id, new.user.id, can_send_messages=True)
                bot.send_message(message.chat.id,"@{}已完成验证，欢迎新成员!".format(new.user.username)) # Welcome message
                Running = False
                callback_init() #verification completed, initialize callback
                break

            else:
                continue

        #Timeout Ban
        if timeout == True:
            bot.ban_chat_member(message.chat.id, new.user.id)
            bot.send_message(message.chat.id,"@{}验证超时，已被ban!".format(new.user.username))
        
        #final_initial
        if not countdownThread.is_alive():
            countdown_init()
                



################################################start########################################################
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
bot.infinity_polling(allowed_updates=util.update_types)



    





