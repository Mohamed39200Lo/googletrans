import telebot
#import requests
#import schedule
#import time
from telebot import types
#from telegram import *
#from telegram.ext import * 
from googletrans import Translator
TA = ["**","* "]
command1=["+translate to arabic"]
command2=["+translate to english"]
bot=telebot.TeleBot("5541021973:AAEx95D4bw8cUUDEZdeUbXzRprdViBmZWZk")
Tol=["/start"]

@bot.message_handler(commands=["english"])
def isMSg (mk) :

	return True
@bot.message_handler(func=isMSg)
def reply(message):
	word = message.text
	words = message.text.split()
	
	markup = types.ReplyKeyboardMarkup()
	sss = types.KeyboardButton("+Translate To English")
	ttt = types.KeyboardButton("+Translate to Arabic")
	xxx = types.KeyboardButton("/start")
	markup.row(xxx)
	markup.row(ttt)
	markup.row(sss)
	if words[0]. lower () in Tol:
		bot.send_message(message.chat.id,"اهلا بك في بوت الترجمة للترجمة الي اللغة العربية : فقط أرسل النص الذي تريد ترجمته وللترجمة إلي الانجليزيه : ضع ** قبل النص مثال**العلم نور ", reply_markup=markup)
		return
	if word[0:21].lower() in command1:
	
		zz=bot.send_message(message.chat.id,"ادخل النص الذي تريد ترجمته")
		return
	if word[0:21].lower() in command2:
		bot.send_message(message.chat.id,"لتترجم النص من اللغة العربية الي الانجليزية اكتب **قبل النص مثال  **العلم نور")
		return
	
	if word[0:2].lower() in TA:
				Trans=Translator ()
				Translation =Trans.translate(word[3:],dest="en")
				bot.reply_to(message, Translation.text)
		
	else:
		
		"""
		#bot.register_next_step_handler(zz, tran )

		def tran(message):
			pp=message.text
			xg=message.chat.id
		"""	
		Trans=Translator ()
		Translation =Trans.translate(word,dest="ar")
		bot.reply_to(message, Translation.text)
	
	
	
		
print ("اهلا بك في بوت الترجمة ")


"""
@bot.message_handler(commands=["start","help"])
def isMSg (mk) :
	return True
@bot.message_handler(func=isMSg)
def reply(message):
	word = message.text
	words = message.text.split()
#	bot.reply_to(message,"hi")
	if words[0].lower() in greetings :
		print (word)
		Trans = Translator ()
		bot.send_message(message.chat.id,"hello")
		Translation =Trans.translate(word,dest="ar")
		print(Translation.text)
@bot.message_handler(commands=["start"])
def isMSg (mk) :
	return True
@bot.message_handler(func=isMSg)
def reply(message):
	word = message.text
	words = message.text.split()
	print ("hh")
	bot.send_message(message.chat.id,"ادخل النص الذي تريد ترجمته")
	Trans = Translator ()
	Translation =Trans.translate(word,dest="ar")
	print(Translation.text)
"""
bot.polling()