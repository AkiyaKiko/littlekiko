import time
import logging
from telebot import util
from telebot import types
from Modules import autoPicture as ap
from telebot.util import quick_markup
from telebot.util import user_link
from telebot import asyncio_helper
from telebot.async_telebot import AsyncTeleBot
import asyncio

# from telebot import asyncio_helper
# asyncio_helper.proxy = 'http://127.0.0.1:10808' #url




################################################initialization#################################################
bot = AsyncTeleBot('TOKEN')

#welcome
call_back_query_data = [None]
call_back_query_user = [None]

################################################command########################################################
#my test module, if needed, discomment it
# @bot.message_handler(commands=['test'])
# def send_testfunc(message : types.Message):

#     bot.send_photo(message.chat.id, "https://floral-disk-7293.nyancatda.workers.dev/img-original/img/2022/08/07/01/10/25/100287825_p1.png")

@bot.message_handler(commands=['start','help'])
async def send_welcome(message : types.Message):
    r_res = await bot.reply_to(message, "你好, "+user_link(message.from_user)+"！我是littlekiko！我的主人是"+"<a href='tg://user?id=5374926976'>秋谷</a>", parse_mode='HTML')
    await asyncio.sleep(0.5)
    s_res = await bot.send_message(message.chat.id, "可以对我使用指令：\n /git --- 查看我的GitHub仓库\n /图 --- 获取一份随机图片\n /色图 --- 获取一份随机色图\n /透 --- 回复你要透的对象就能自动透了\n /ban --- 管理员回复你想要ban的对象\n")
    await asyncio.sleep(15)
    await bot.delete_message(chat_id = message.chat.id, message_id = r_res.message_id)
    await asyncio.sleep(0.3)
    await bot.delete_message(chat_id = message.chat.id, message_id = s_res.message_id)


@bot.message_handler(commands=['ban'])
async def ban_someone(message : types.Message):
    ban_id = message.reply_to_message.from_user.id
    ban_fn = message.reply_to_message.from_user.first_name
    await bot.ban_chat_member(message.chat.id, user_id=message.reply_to_message.from_user.id,until_date=60)
    await asyncio.sleep(0.3)
    await bot.send_message(message.chat.id, "Ban "+"<a href='tg://user?id={}'>{}</a>".format(ban_id,ban_fn)+"60s", parse_mode='HTML')



#tou!
@bot.message_handler(commands=['透', '内射', '干烂'])
async def tou(message : types.Message):
    command = message.text.replace('/','')
    await bot.send_message(message.chat.id,user_link(message.from_user)+'{}了'.format(command)+user_link(message.reply_to_message.from_user), parse_mode='HTML')

#picture
@bot.message_handler(commands=['图'])
async def send_picture(message : types.Message):
    url = 'https://api.nyan.xyz/httpapi/sexphoto'
    params = {'num': '1', 'r18': 'false'}
    photo_url = ap.getAutoPicture(url, params)
    await bot.send_photo(message.chat.id, photo_url, timeout=100)

#ero_picture
@bot.message_handler(commands=['色图'])
async def send_ero_picture(message : types.Message):
    url = 'https://api.nyan.xyz/httpapi/sexphoto'
    params = {'num': '1', 'r18': 'true'}
    photo_url = ap.getAutoPicture(url, params)
    await bot.send_photo(message.chat.id, photo_url, timeout=100)
    

@bot.message_handler(commands=['git'])
async def send_git_repo(message : types.Message):
    git_repository = 'https://github.com/AkiyaKiko/littlekiko'
    await bot.reply_to(message, "<a href='{}'>这是我的Github仓库地址</a>".format(git_repository), parse_mode='HTML')

################################################keyword########################################################
#sese rebot !! seigo    
@bot.message_handler(regexp='色色')
async def repeat_reply(message):
    #group sese
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        await bot.reply_to(message, '色色！')
    #pm sese
    if message.chat.type == 'private':
        await bot.reply_to(message, '啊哈！虽然是私聊，但还是不能对我单独色色哦！')

#good night
@bot.message_handler(regexp='晚安')
async def haveAGoodnight(message):
    await bot.reply_to(message, '晚安！')

#Subscription
@bot.message_handler(regexp='订阅')
async def supportSub(message):
    await bot.reply_to(message, '啊哈，以下是免费的订阅链接哦：https://sub.sharecentre.online/sub 公益链接提供者：@ShareCentrePro')

################################################welcome########################################################
#generate inline keyboard
def gen_markup():
    markup = quick_markup({
        '点击验证 Authentication':{'callback_data':'verify_click'},
        '由可爱的kiko手动通过 Passed By Admin':{'callback_data':'admin_verify_click'},
        
    },row_width=2)
    return markup

#handle callback
@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call : types.CallbackQuery):
    call_back_query_data[0] = call.data
    call_back_query_user[0] = call.from_user

# #verification countdown
# def countdown():
#     for count in range(0,30):
#         global Running
#         global timeout
#         if Running == False:
#             break
#         elif Running == True and timeout == False:
#             asyncio.sleep(1)
#         elif Running == True and count == 29:
#             timeout = True
# #initialize Running and timeout
# def countdown_init():
#     global Running,timeout
#     Running = True
#     timeout = False

# #initialize the callback data and user
# def callback_init():
#     global call_back_query_data,call_back_query_user
#     call_back_query_data = [None]
#     call_back_query_user = [None]
        
#verify the click callback
def verify(new_user : types.User):
    if call_back_query_data[0] == 'verify_click' and call_back_query_user[0].username == new_user.username:
        return True
    elif  call_back_query_data[0] == 'admin_verify_click' and call_back_query_user[0].username == 'akiyakiko':
        return True
    

#chat_member_handler. When status changes, telegram gives update. check status from old_chat_member and new_chat_member.
@bot.chat_member_handler()
async def chat_m(message: types.ChatMemberUpdated):
    old = message.old_chat_member
    new = message.new_chat_member
    if new.status == "member":

        # bot.send_message(message.chat.id,"Hello @{name}!".format(name=new.user.first_name)) # Welcome message
        send_ver = await bot.send_message(message.chat.id, user_link(message.from_user)+"你好,请完成验证，否则永久禁言 Hello, please finish the verification", reply_markup=gen_markup(), parse_mode='HTML')
        await bot.restrict_chat_member(message.chat.id, new.user.id, until_date=999999999999, can_send_messages=False, can_send_media_messages=False)
        for cd in range(0,3000):
            result = verify(new.user)
            if result == True and cd != 2999:
                await bot.restrict_chat_member(message.chat.id, new.user.id, can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
                send_res = await bot.send_message(message.chat.id, user_link(message.from_user)+"已完成验证，欢迎新成员! Verfied! Welcome!", parse_mode='HTML')
                await asyncio.sleep(15)
                await bot.delete_message(chat_id = message.chat.id,message_id = send_ver.message_id)
                await asyncio.sleep(0.5)
                await bot.delete_message(chat_id = message.chat.id,message_id = send_res.message_id)
                break
            elif result != True and cd != 2999:
                await asyncio.sleep(0.01)
            elif cd == 2999:
                await bot.ban_chat_member(chat_id = message.chat.id,user_id=new.user.id)
                send_res = await bot.send_message(message.chat.id, user_link(message.from_user)+"未完成验证，已Ban!\nBanned becasue of Verification TimeOut!\n请私聊管理员处理!\nPlease PM Admins to remove the restriction!", parse_mode='HTML')
                await asyncio.sleep(15)
                await bot.delete_message(chat_id = message.chat.id,message_id = send_ver.message_id)
                # await asyncio.sleep(0.5)
                # await bot.delete_message(chat_id = message.chat.id,message_id = send_res.message_id)
                break

        # #Countdown_thread
        # countdownThread = threading.Thread(target=countdown)
        # countdownThread.start()
        
        # #Verification_complete
        # while countdownThread.is_alive():
        #     result = verify(new.user)
        #     if result == True:
        #         await bot.restrict_chat_member(message.chat.id, new.user.id, can_send_messages=True, can_send_media_messages=True)
        #         await bot.send_message(message.chat.id, user_link(message.from_user)+"已完成验证，欢迎新成员!", parse_mode='HTML') # Welcome message
        #         Running = False
        #         callback_init() #verification completed, initialize callback
        #         break

        #     else:
        #         continue

        # #Timeout Ban
        # if timeout == True:
        #     bot.send_message(message.chat.id, user_link(message.from_user)+"验证超时，已被ban!", parse_mode='HTML')
        #     bot.kick_chat_member(message.chat.id, new.user.id)
            
        
        # #final_initial
        # if not countdownThread.is_alive():
        #     countdown_init()
                



################################################start########################################################
# logger = AsyncTeleBot.logger
# AsyncTeleBot.logger.setLevel(logging.DEBUG)
# bot.infinity_polling(allowed_updates=util.update_types)
asyncio.run(bot.polling(allowed_updates=util.update_types))


    





