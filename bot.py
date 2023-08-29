import os
import telebot
import aspose.words as aw
from telebot import types
import random
import re
import settings

bot = telebot.TeleBot(settings.KEY)

def func(form, mt_):
  global answer, na, doc_user
  doc = aw.Document(f"C:/Users/dmitriy/OneDrive/Рабочий стол/python1/Програмист/{form}")
  name_answer = str(random.random())
  na = name_answer
  answer = doc.save(f"{na}{mt_}")
  doc_user = na + mt_


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
	try:
	    chat_id = message.chat.id
	    file_info = bot.get_file(message.document.file_id)
	    downloaded_file = bot.download_file(file_info.file_path)
	    

	    src = 'C:/Users/dmitriy/OneDrive/Рабочий стол/python1/Програмист/telbot' + message.document.file_name;
	    with open(src, 'wb') as new_file:
	        new_file.write(downloaded_file)
	        file_name, file_extension = os.path.splitext(new_file.name)
	        global form
	        form = os.path.basename(new_file.name)
	        size = os.path.getsize(new_file.name)
	        print(size)

	    bot.reply_to(message, "Ваш формат: " + file_extension + "\nРазмер файла в байтах: " + str(size) + "\nВыберите формат для конвертации: \n/pdf \n/docx \n/txt \n/jpeg")
	except Exception as e:
	    bot.reply_to(message, e)


@bot.message_handler(commands = ["start", "convert"])
def start(message):
	if message.text == "/start":
		bot.send_message(message.chat.id, "Привет, здесь ты можешь конвертировать файл" 
			" напиши команду /convert в чат", parse_mode = "markdown")
	elif message.text == "/convert":
		bot.send_message(message.chat.id, "Загрузите файл")	


@bot.message_handler(commands = ["pdf", "docx", "txt", "jpeg"])
def convert(message):
	mt = message.text.replace("/", ".")
	print(mt)
	func(form, mt)
	bot.send_message(message.chat.id, "Ваш файл обрабатывается \nЧто бы поулчить файл, напиши команду /getfile ")
	#if message.text == "/pdf":

@bot.message_handler(commands = ["getfile"])
def com(message):
	a = open(f"{doc_user}", "rb")
	bot.send_document(message.chat.id, a)
	

@bot.message_handler()
def get_user_text(message):
	if message.text == "Hello":
		bot.send_message(message.chat.id, "Привет, здесь ты можешь конвертировать файл", parse_mode = "markdown")
	elif message.text == "help":
		print(message)
		bot.send_message(message.chat.id, "Cкоро команда заработает, пока не придумал, что она делает", parse_mode = "markdown")

bot.polling(none_stop = True, interval = 0)


