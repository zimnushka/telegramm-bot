# {'content_type': 'text',
#  'id': 24, 'message_id': 24,
#   'from_user': {'id': 722421615, 'is_bot': False, 'first_name': 'Зимнухов', 'username': 'KRD_KIRILL_ZIMNUKHOV', 'last_name': 'Кирилл', 'language_code': 'ru', 'can_join_groups': None, 'can_read_all_group_messages': None, 'supports_inline_queries': None},
#    'date': 1617535696, 
#    'chat': {'id': 722421615, 'type': 'private', 'title': None, 'username': 'KRD_KIRILL_ZIMNUKHOV', 'first_name': 'Зимнухов', 'last_name': 'Кирилл', 'photo': None, 'bio': None, 'description': None, 'invite_link': None, 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None}, 
#   'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'reply_to_message': None, 'edit_date': None, 'media_group_id': None, 'author_signature': None, 'text': 'eweew', 'entities': None, 'caption_entities': None, 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 'reply_markup': None, 'json': {'message_id': 24, 'from': {'id': 722421615, 'is_bot': False, 'first_name': 'Зимнухов', 'last_name': 'Кирилл', 'username': 'KRD_KIRILL_ZIMNUKHOV', 'language_code': 'ru'}, 'chat': {'id': 722421615, 'first_name': 'Зимнухов', 'last_name': 'Кирилл', 'username': 'KRD_KIRILL_ZIMNUKHOV', 'type': 'private'}, 'date': 1617535696, 'text': 'eweew'}}
import sys
sys.path.insert(0, 'C:/git/')

import telebot
import config

bot = telebot.TeleBot(config.tokenApi)

users = []
mailing = False
usersLen = int(0)

def addUser(id):
	usersLen = int(len(users))
	#проверяем наличие данного пользователя в массиве, если его нет то добавляем.
	print(usersLen)
	for i in range(usersLen):
		if users[i] == id:
			return
	users.append(id)
	print(users)

def buttons(message):
	markup = telebot.types.InlineKeyboardMarkup()
	markup.add(telebot.types.InlineKeyboardButton(text='Три', callback_data=3))
	markup.add(telebot.types.InlineKeyboardButton(text='Четыре', callback_data=4))
	markup.add(telebot.types.InlineKeyboardButton(text='Пять', callback_data=5))
	# bot.send_message(message.chat.id, message.caption, reply_markup=markup)
	bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)

def adminButtons(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Начать рассылку')
    bot.send_message(message.chat.id, 'Для начала рассылки нажмите кноку "Начать рассылку"', reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def send_welcome(message):
   addUser(message.from_user.id)
   bot.reply_to(message, f'Я бот носочки ОПТ. Приятно познакомиться, {message.from_user.first_name} {message.from_user.last_name}. Я буду сообщать вам о новинках, а вы сможете делать быстрые заказы!')

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):

   bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за честный ответ!')
   answer = ''
   if call.data == '3':
      answer = '3!'
   elif call.data == '4':
      answer = '4!'
   elif call.data == '5':
      answer = '5!'

   bot.send_message(call.message.chat.id, answer)
   bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global mailing
	print(mailing)
	usersLen = int(len(users))
	if message.from_user.id == 722421615:
		if message.text=='Начать рассылку':
			bot.send_message(message.chat.id, 'Отправте фото(желательно одно, если их много то сделайте предворительно коллаж) и напишите текст, а я его перепралю')
			mailing = True
		elif mailing==True:
			buttons(message)
			mailing = False
		else:
			adminButtons(message)
		

@bot.message_handler(content_types=['photo'])
def get_text_messages(message):
	usersLen = int(len(users))
	if message.from_user.id == 722421615:
		bot.forward_message(message.chat.id, message.chat.id, message.message_id)
		buttons(message)
		# bot.send_photo(message.chat.id, message.photo)
		
bot.polling(none_stop=True)