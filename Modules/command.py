from . import bot
from . import autoPicture as ap
from telebot import types



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





'''
#Chatgpt
@bot.message_handler(commands=['chat'])
def chatgpt(message):
    conversation_id = "[]" 
    ans = rchat.chatGPT(message.text, conversation_id)
    bot.reply_to(message,ans)
'''