from . import bot
from . import autoPicture as ap



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "你好！我是littlekiko！我的主人是https://t.me/akiyakiko")

#tou!
@bot.message_handler(commands=['透', '内射', '干烂'])
def tou(message):
    command = message.text.replace('/','')
    bot.reply_to(message,'{} {}了 {}'.format(message.from_user.first_name, command, message.reply_to_message.from_user.first_name))

#picture
@bot.message_handler(commands=['图'])
def send_picture(message):
    url = 'https://api.nyan.xyz/httpapi/sexphoto'
    params = {'num': '1', 'r18': 'false'}
    bot.reply_to(message, ap.getAutoPicture(url,params))

#ero_picture
@bot.message_handler(commands=['色图'])
def send_ero_picture(message):
    url = 'https://api.nyan.xyz/httpapi/sexphoto'
    params = {'num': '1', 'r18': 'true'}
    bot.reply_to(message, ap.getAutoPicture(url, params))





'''
#Chatgpt
@bot.message_handler(commands=['chat'])
def chatgpt(message):
    conversation_id = "f019f0de-0971-42cf-9b4c-3c62c3d3a8f8" 
    ans = rchat.chatGPT(message.text, conversation_id)
    bot.reply_to(message,ans)
'''