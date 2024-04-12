import telebot
from telebot import types
import random


TO_CHAT_ID = -4139752150
bot = telebot.TeleBot('6982204170:AAEhoSX0YgmYoSNMLK1ePhQPKN88Ork-qmk')
points = 0
requests_queue = []


@bot.message_handler(commands=['feedback'])
def welcome(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте!, {0.first_name}!\nЯ, бот созданный, чтобы помочь улучшить работу сотрудников зоопарка. Если "
                     "у Вас имеется отзыв о работе сотрудников, то напишите его ниже".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.register_next_step_handler(message, help_bot)

# Функция, отправляющая вопрос от пользователя в чат поддержки
def help_bot(message):
    requests_queue.append((message.message_id, message.chat.id))
    bot.forward_message(TO_CHAT_ID, message.chat.id, message.message_id)
    markup_inline = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{message.chat.id}')
    ]])
    bot.send_message(TO_CHAT_ID, f"Действие:", reply_markup=markup_inline)
    bot.register_next_step_handler(message, help_bot)



@bot.message_handler(commands=["requests"], func=lambda m: int(m.chat.id) == int(TO_CHAT_ID))
def all_messages(message):
    bot.send_message(message.chat.id, "Доступные запросы:")
    for i, req in enumerate(requests_queue):
        bot.forward_message(TO_CHAT_ID, req[1], req[0])
        markup_inline = types.InlineKeyboardMarkup([[
            types.InlineKeyboardButton(text='Ответить', callback_data=f'answer{req[1]}')
        ]])
        bot.send_message(message.chat.id, f"Действие:", reply_markup=markup_inline)


def send_answer(message: types.Message, call, chat_id):
    bot.send_message(call.message.chat.id, "Ответ отправлен!")
    bot.send_message(chat_id, message.text)
    for i, req in enumerate(requests_queue):
        if int(req[1]) == int(chat_id):
            del requests_queue[i]


@bot.callback_query_handler(func=lambda call: True)
def answer_callback(call: types.CallbackQuery):
    if call.data.startswith("answer"):
        chat_id = int(call.data[6:])

        bot.send_message(call.message.chat.id, "Отправьте ответ на запрос")
        bot.register_next_step_handler(call.message, lambda msg: send_answer(msg, call, chat_id))






words1 = ["Тааак", "Я уже догадываюсь, какое твоё животное :)", "А, что, если..."]
random1 = random.choices(words1)
random2 = random1[0] or random1[1] or random1[2]

words2 = ["Ну-ка, поподробней", "Вот-вот и мы узнаем, кто тебе нравится)", "Ах, вот оно что :D"]
random1_ = random.choices(words2)
random2_ = random1_[0] or random1_[1] or random1_[2]


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton("Начать викторину!"))
    bot.reply_to(message, "Привет, друг!\nЧтобы начать, нажми кнопку!", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

@bot.message_handler(commands=['hippopotamus'])
def info_bear(message):
    file = open('./begemot.jpeg', 'rb')
    bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=['panda'])
def info_panda(message):
    file = open('./panda.jpg', 'rb')
    bot.send_photo(message.chat.id, file)


@bot.message_handler(commands=['ratel'])
def info_panda(message):
    file = open('./ratel.jpg', 'rb')
    bot.send_photo(message.chat.id, file)

@bot.message_handler(content_types=["text"])
def on_click(message):
    global points
    global random2
    global random2_
    if message.text == "Начать викторину!":
        points = 0
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Плохо лажу с людьми")
        item2 = types.KeyboardButton("Раздражительность")
        item3 = types.KeyboardButton("Любопытство")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "1) Какая твоя отрицательная черта?", reply_markup=markup)



    if message.chat.type == "private":
        # Отслеживаем 1-ый вопрос:
        if message.text == "Плохо лажу с людьми":
            bot.send_message(message.chat.id, random2)
            points += 1

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Мясо, рыба")
            item2 = types.KeyboardButton("Салаты, легкие закуски")
            item3 = types.KeyboardButton("Сладости")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "2) Твои предпочтения в еде?", reply_markup=markup)

        elif message.text == "Раздражительность":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Ах, вот оно что :D")
            points += 2

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Мясо, рыба")
            item2 = types.KeyboardButton("Салаты, легкие закуски")
            item3 = types.KeyboardButton("Сладости")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "2) Твои предпочтения в еде?", reply_markup=markup)

        elif message.text == "Любопытство":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "А вот это уже интересно...)")
            points += 3

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Мясо, рыба")
            item2 = types.KeyboardButton("Салаты, легкие закуски")
            item3 = types.KeyboardButton("Сладости")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "2) Твои предпочтения в еде?", reply_markup=markup)

        # Отслеживаем 2-ой вопрос:
        if message.text == "Сладости":
            bot.send_message(message.chat.id, random2)
            points += 1

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Сильный")
            item2 = types.KeyboardButton("Гордый")
            item3 = types.KeyboardButton("Хитрый")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "3) Каким образом можно охарактеризовать твоего любимого зверя?", reply_markup=markup)

        elif message.text == "Салаты, легкие закуски":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Нужно больше подробностей!")
            points += 2

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Сильный")
            item2 = types.KeyboardButton("Гордый")
            item3 = types.KeyboardButton("Хитрый")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "3) Каким образом можно охарактеризовать твоего любимого зверя?", reply_markup=markup)

        elif message.text == "Мясо, рыба":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Скоро мы всё про тебя узнаем ;)")
            points += 3

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Сильный")
            item2 = types.KeyboardButton("Гордый")
            item3 = types.KeyboardButton("Хитрый")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "3) Каким образом можно охарактеризовать твоего любимого зверя?", reply_markup=markup)

        # Отслеживаем 3-ий вопрос:
        if message.text == "Гордый":
            bot.send_message(message.chat.id, random2)
            points += 1

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Честь")
            item2 = types.KeyboardButton("Одиночество")
            item3 = types.KeyboardButton("Изворотливость")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "4) Выбирай не задумываясь:", reply_markup=markup)

        elif message.text == "Хитрый":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Ну-ка, поподробней -_-")
            points += 2

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Честь")
            item2 = types.KeyboardButton("Одиночество")
            item3 = types.KeyboardButton("Изворотливость")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "4) Выбирай не задумываясь:", reply_markup=markup)

        elif message.text == "Сильный":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Осталось совсем немного!")
            points += 3

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Честь")
            item2 = types.KeyboardButton("Одиночество")
            item3 = types.KeyboardButton("Изворотливость")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "4) Выбирай не задумываясь:", reply_markup=markup)

        # Отслеживаем 4-ый вопрос:
        if message.text == "Одиночество":
            bot.send_message(message.chat.id, random2)
            points += 1

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Адреналин")
            item2 = types.KeyboardButton("Лидерство всегда и везде")
            item3 = types.KeyboardButton("Большая и дружная семья")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "Что для тебя интереснее?", reply_markup=markup)

        elif message.text == "Честь":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Ага.. дальше")
            points += 2

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Адреналин")
            item2 = types.KeyboardButton("Лидерство всегда и везде")
            item3 = types.KeyboardButton("Большая и дружная семья")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "Что для тебя интереснее?", reply_markup=markup)

        elif message.text == "Изворотливость":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Далеко пойдешь :D")
            points += 3

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Адреналин")
            item2 = types.KeyboardButton("Лидерство всегда и везде")
            item3 = types.KeyboardButton("Большая и дружная семья")
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, "Что для тебя интереснее?", reply_markup=markup)

        # Отслеживаем 5-ый вопрос:
        if message.text == "Большая и дружная семья":
            bot.send_message(message.chat.id, random2)
            points += 1

            if points <= 5:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самка карликового бегемота Глория!\nГлории всего 3 месяца, но она уже жуёт арбузы и любит свежую тыкву :)\nЕсли хочешь стать её опекуном, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Глорию нажми на /hippopotamus\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            elif points <= 10:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самец большой панды Джек!\nДжеку 5 лет, он еще молод, а потому ему нужно много свежих фруктов и сочный бамбук!\nЕсли хочешь стать его опекуном, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Джека нажми на /panda\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            elif points <= 15:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самка медоеда Милка!\nУ Милки недавно появились детеныши, ей нужно очень много сил, чтобы научить премудростям существования в этом мире своих малышей\nМилка хищник и ест белковую пищу\nЕсли хочешь опекать её и её малышей, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Милку нажми на /ratel\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            else:
                return


        elif message.text == "Лидерство всегда и везде":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Похвально!")
            points += 2

            if points <= 5:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самка карликового бегемота Глория!\nГлории всего 3 месяца, но она уже жуёт арбузы и любит свежую тыкву :)\nЕсли хочешь стать её опекуном, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Глорию нажми на /hippopotamus\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            elif points <= 10:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самец большой панды Джек!\nДжеку 5 лет, он еще молод, а потому ему нужно много свежих фруктов и сочный бамбук!\nЕсли хочешь стать его опекуном, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Джека нажми на /panda\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            elif points <= 15:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самка медоеда Милка!\nУ Милки недавно появились детеныши, ей нужно очень много сил, чтобы научить премудростям существования в этом мире своих малышей\nМилка хищник и ест белковую пищу\nЕсли хочешь опекать её и её малышей, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Милку нажми на /ratel\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            else:
                return



        elif message.text == "Адреналин":
            bot.send_message(message.chat.id, random2_)
            bot.send_message(message.chat.id, "Мощно!")
            points += 3

            if points <= 5:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самка карликового бегемота Глория!\nГлории всего 3 месяца, но она уже жуёт арбузы и любит свежую тыкву :)\nЕсли хочешь стать её опекуном, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Глорию нажми на /hippopotamus\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            elif points <= 10:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самец большой панды Джек!\nДжеку 5 лет, он еще молод, а потому ему нужно много свежих фруктов и сочный бамбук!\nЕсли хочешь стать его опекуном, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Джека нажми на /panda\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            elif points <= 15:
                bot.send_message(message.chat.id,
                                 f'Вот мы и закончили викторину!\nПо её результатам, твоё животное - самка медоеда Милка!\nУ Милки недавно появились детеныши, ей нужно очень много сил, чтобы научить премудростям существования в этом мире своих малышей\nМилка хищник и ест белковую пищу\nЕсли хочешь опекать её и её малышей, то вот контакты сотрудников, с которыми ты можешь связаться: XXXXXX\nА, чтобы посмотреть на Милку нажми на /ratel\nЕсли хочешь снова пройти тест, нажми на /start\n И обязательно оставь отзыв, нажми на /feedback!')
            else:
                return





bot.polling()
















