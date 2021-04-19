import sys
sys.path.insert(0, 'C:/git/')

import telebot
import config
import sqlite3
import random
import string
import time

db = sqlite3.connect('telegramDb.db', check_same_thread=False)
sql = db.cursor()
# sql.execute("INSERT INTO `users` (`user_id`, `status`) VALUES(?,?)", (user_id,bool))
bot = telebot.TeleBot(config.tokenApi)

users = []
admins = []
allUsers = []

def update():	
	global users
	global admins
	allUsers = []
	for value in sql.execute("SELECT user_id FROM `users`"):
		allUsers.append(value[0])
	db.commit()
	users = []
	for value in sql.execute("SELECT user_id FROM `users` WHERE `status` = ?", [1]):
		users.append(value[0])
	db.commit()
	admins = []
	for value in sql.execute("SELECT user_id FROM `users` WHERE `status` = ?", [2]):
		admins.append(value[0])
	db.commit()
update()
mail = False
buy = False
comm = False

recordBuy = False
recordComm = False
letters = string.ascii_lowercase
randStr=str()
def addUser(id, message):
	allusersLen = int(len(allUsers))
	for i in range(allusersLen):
		if allUsers[i] == id:
			usersLen = int(len(users))
			for e in range(usersLen):
				if users[e] == id:
					keyButtons(message,1,1)
					return
			sql.execute("UPDATE `users` SET `status` = 1 WHERE `user_id` = ?", [id])
			db.commit()
	adminsLen = int(len(admins))
	for i in range(adminsLen):
		if admins[i] == id:
			keyButtons(message,1,2)
			return
	sql.execute("INSERT INTO `users` (`user_id`, `status`) VALUES(?,?)", (id,1))
	db.commit()
	keyButtons(message,1,1)
	update()

def checkAdmin(id):
	adminsLen = int(len(admins))
	#проверяем наличие данного пользователя в массиве, если его нет то добавляем.
	print(adminsLen)
	for i in range(adminsLen):
		if admins[i] == id:
			print("admin")
			return 1
	return 0

def buttons(message, messageid):
	markup = telebot.types.InlineKeyboardMarkup()
	markup.add(telebot.types.InlineKeyboardButton(text='Заказать', callback_data=1))
	markup.add(telebot.types.InlineKeyboardButton(text='Комментировать', callback_data=2))
	bot.send_message(messageid, 'Выберите действие', reply_markup=markup)

def mailing(message, messageid):
	usersLen = int(len(users))
	for i in range(usersLen):
		bot.forward_message(users[i], message.chat.id, messageid)
		buttons(message, users[i])
		time.sleep(1)
 
def checMail(message):
	global mail
	global messageid
	if checkAdmin(message.from_user.id)==1:
		if message.text=='Рассылка':
			bot.send_message(message.chat.id, 'Отправте фото(желательно одно, если их много то сделайте предворительно коллаж) и напишите текст, а я его переправлю')
			mail = True
		elif mail==True:
			if message.text == 'нет':
				bot.send_message(message.chat.id, 'Подготовте сообщение, я вас всегда жду)')
				mail = False
			elif message.text == 'да':
				global randStr
				randStr = (''.join(random.choice(letters) for i in range(4)))
				bot.send_message(message.chat.id, 'Пересылаю сообщение (' +randStr+' - это код сообщения в будущем вы сожете посмотреть комментарии и заказы по этой рассылке)')
				mailing(message, messageid)
				keyButtons(message,1,2)
				mail = False
			else:
				keyButtons(message,2,2)
				bot.forward_message(message.chat.id, message.chat.id, message.message_id)
				messageid =  message.message_id
		elif message.text=='Заказы':
			bot.send_message(message.chat.id, 'Напишите код вашей рассылки')
			buy = True



def keyButtons(message,types,status):
	if status == 1:
		if types == 1:
		   keyboard = telebot.types.ReplyKeyboardMarkup(True)
		   keyboard.row('отменить подписку')
		   bot.send_message(message.chat.id, 'Если вы отмените подписку, то не будет приходить рассылка', reply_markup=keyboard)
		elif types == 2:
			print('types 2')
	elif status == 2:
		if types == 1:
		   keyboard = telebot.types.ReplyKeyboardMarkup(True)
		   keyboard.row('Рассылка', 'Заказы', 'Комментарии')
		   bot.send_message(message.chat.id, 'Выберите действие', reply_markup=keyboard)
		elif types == 2:
			keyboard = telebot.types.ReplyKeyboardMarkup(True)
			keyboard.row('да', 'нет')
			bot.send_message(message.chat.id, 'ВОТ ТАК БУДЕТ ВЫГЛЯДЕТЬ ВАШЕ СООБЩЕНИЕ, НАЧАТЬ РАССЫЛКУ?(нажмите на кнопку)', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
   bot.reply_to(message, f'Я бот носочки ОПТ. Приятно познакомиться, {message.from_user.first_name} {message.from_user.last_name}. Я буду сообщать вам о новинках, а вы сможете делать быстрые заказы!')
   addUser(message.from_user.id, message)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

   bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за ответ!')
   answer = ''
   global recordBuy
   global recordComm
   if call.data == '1':
      answer = 'Напишите текст, например: "30 гольф с звездой, 20 носков черного цвета"'
      recordBuy = True
   elif call.data == '2':
      answer = 'Напишите текст, например: "Я бы хотел носки в полосочку, но серые"'
      recordComm = True

   bot.send_message(call.message.chat.id, answer)
   bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	if checkAdmin(message.from_user.id)==1:
		checMail(message)
	else:
		global recordBuy
		global recordComm
		if recordBuy == True:
			firstName = str(message.from_user.first_name)
			secondName = str(message.from_user.last_name)
			name = str(firstName + ' ' + secondName)
			description = message.text
			sql.execute("INSERT INTO `notes` (`name`, `description`, `id_note`, `type`) VALUES(?,?,?,1)", (name, description,randStr))
			db.commit()
			recordBuy =False
		elif recordComm == True:
			firstName = str(message.from_user.first_name)
			secondName = str(message.from_user.last_name)
			name = str(firstName + ' ' + secondName)
			description = message.text
			sql.execute("INSERT INTO `notes` (`name`, `description`, `id_note`, `type`) VALUES(?,?,?,2)", (name, description,randStr))
			db.commit()
			recordComm = False

@bot.message_handler(content_types=['audio'])
def get_text_messages(message):
	checMail(message)

@bot.message_handler(content_types=['document'])
def get_text_messages(message):
	checMail(message)

@bot.message_handler(content_types=['video'])
def get_text_messages(message):
	checMail(message)

@bot.message_handler(content_types=['photo'])
def get_text_messages(message):
	checMail(message)
	
bot.polling(none_stop=True)