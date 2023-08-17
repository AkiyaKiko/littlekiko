from . import bot

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




