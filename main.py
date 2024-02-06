from telebot import *
from checker import *

token = '6706621045:AAFXVQIU3AyGACHM00FRJHEGxdowxjGZuvk'

# Я - 729371813
# Саня - 275280940

bot = telebot.TeleBot(token)

application_dict = {}

dict_disp_photos = {}

user_photos_dict = {}

counter_dict = {}

clear()


# SLASH COMMANDS
@bot.message_handler(commands=['reply'])
def reply(message):
    if isDispatcher(message.chat.id):
        bot.reply_to(message, 'Введите id')
        counter_dict[str(message.chat.id)] = 15


@bot.message_handler(commands=['start', 'help'])
def start(message):
    if not isDispatcher(message.chat.id):
        counter_dict[str(message.chat.id)] = 1
        writeUser(message.chat.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton("Проблема с уборкой", callback_data='first_disp')
        btn2 = types.InlineKeyboardButton("Другое", callback_data='second_disp')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, "Здравствуйте!\nПожалуйста выберите к какому типу относится ваша заявка",
                         reply_markup=markup)
        user_photos_dict[str(message.chat.id)] = []
        application_dict[str(message.chat.id)] = {
            "street": "",
            "num": '',
            "problem": '',
            "app_num": '',
            "app_id": '',
            "disp_type": ''
        }
    else:
        addDispatcher(message.chat.id)
        bot.send_message(message.chat.id,
                         'Привет, диспетчер. Чтобы принять заявку - /reply id. Чтобы отправить фото заявителю - /done id')
        dict_disp_photos[str(message.chat.id)] = []
        counter_dict[str(message.chat.id)] = 14


@bot.message_handler(commands=['done'])
def done(message):
    if isDispatcher(message.chat.id):
        bot.reply_to(message, 'Введите id')
        counter_dict[str(message.chat.id)] = 16
        dict_disp_photos[str(message.chat.id)] = []


####

@bot.message_handler(func=lambda message: isDispatcher(message.chat.id) and not checkDispatcher(message.chat.id))
def no_start(message):
    bot.reply_to(message, "Нажмите /start")


@bot.message_handler(func=lambda message: isUser(message.chat.id) == 0 and not isDispatcher(message.chat.id))
def no_start(message):
    bot.reply_to(message, "Пожалуйста, для создания заявки нажмите\n/start")


@bot.message_handler(func=lambda message: not isDispatcher(message.chat.id) and counter_dict[str(message.chat.id)] == 0)
def zero_cnt(message):
    bot.reply_to(message, "Пожалуйста, для создания заявки нажмите\n/start")


@bot.message_handler(func=lambda message: check_street(message.text) == 100 and len(
    message.text) > 1 and counter_dict[str(message.chat.id)] == 1 and not isDispatcher(message.chat.id))
def street_input(message):
    if not isDispatcher(message.chat.id):
        application_dict[str(message.chat.id)]['street'] = message.text
        counter_dict[str(message.chat.id)] = 2
        bot.reply_to(message, "Отлично, теперь введите номер дома.")


@bot.message_handler(
    func=lambda message: check_street(message.text) < 100 and not isDispatcher(message.chat.id) and counter_dict[
        str(message.chat.id)] == 1 and message.text.lower() != 'да' and message.text.lower() != 'нет')
def non_street_input(message):
    bot.reply_to(message,
                 f"Вашей улицы нет в нашей базе обслуживания.\nВозможно, вы хотели написать ул. {getMostSimilar(message.text)}?")
    application_dict[str(message.chat.id)]['street'] = getMostSimilar(message.text)


@bot.message_handler(
    func=lambda message: message.text[0].isdigit() and not isDispatcher(message.chat.id) and check_house(
        application_dict[str(message.chat.id)]['street'], message.text) and counter_dict[str(message.chat.id)] == 2)
def num_input(message):
    application_dict[str(message.chat.id)]["house_num"] = message.text.strip(' ')
    counter_dict[str(message.chat.id)] = 3
    bot.reply_to(message,
                 "Отлично, теперь опишите проблему!\n-Пожалуйста, <u><b>не прикрепляйте фото сейчас</b></u>, это нужно будет сделать после описания проблемы.\n\n-Можете указать номер мобильного телефона для связи с Вами, если требуется.",
                 parse_mode="html")


@bot.message_handler(
    func=lambda message: message.text[0].isdigit() and not isDispatcher(message.chat.id) and check_house(
        application_dict[str(message.chat.id)]['street'],
        message.text) == 0 and counter_dict[str(message.chat.id)] == 2)
def non_num_input(message):
    bot.reply_to(message, "Дома с таким номером нет в нашей базе обслуживания.\nПожалуйста, проверьте номер дома.")


@bot.message_handler(content_types=['text'])
def parse(message):
    if message.content_type == 'text':
        if counter_dict[str(message.chat.id)] == 3:
            application_dict[str(message.chat.id)]['problem'] = message.text
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("Да", callback_data='yes')
            btn2 = types.InlineKeyboardButton("Нет", callback_data='no')
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, "Желаете прикрепить фото к вашей заявке?", reply_markup=markup)
        elif message.text.lower() == "да" and counter_dict[str(message.chat.id)] == 1:
            bot.reply_to(message,
                         f"Отлично, заявка составляется по ул. <b><u>{application_dict[str(message.chat.id)]['street']}</u></b>.\n\nТеперь введите номер дома.",
                         parse_mode="html")
            counter_dict[str(message.chat.id)] = 2
        elif message.text.lower() == "нет" and counter_dict[str(message.chat.id)] == 1:
            bot.reply_to(message, "Пожалуйста, введите название улицы.")
        elif counter_dict[str(message.chat.id)] == 1:
            bot.reply_to(message,
                         f"Вашей улицы нет в базе обслуживания, возможно, вы имели в виду улицу {getMostSimilar(message.text)}?\nЕсли да - напишите её название как указано в вопросе-уточнении.")
            bot.register_next_step_handler(message, non_street_input)
        elif counter_dict[str(message.chat.id)] < 3:
            bot.reply_to(message, "Вы не ввели номер дома.")
        elif isDispatcher(message.chat.id) and message.text[0].isdigit():
            global repliable_id
            if len(message.text) > 2:
                repliable_id = int(message.text)
                if counter_dict[str(message.chat.id)] == 15:
                    if isUser(repliable_id):
                        bot.send_message(repliable_id, 'Ваша заявка была принята в работу!')
                        bot.reply_to(message, "Заявка принята")
                    else:
                        bot.reply_to(message, "Такой человек к нам не обращался")

                if counter_dict[str(message.chat.id)] == 16:
                    markup = types.InlineKeyboardMarkup(row_width=1)
                    btn1 = types.InlineKeyboardButton("Да(пизда)", callback_data='yes')
                    btn2 = types.InlineKeyboardButton("Нет", callback_data='nea')
                    markup.add(btn1, btn2)
                    bot.send_message(message.chat.id, "Желаете прикрепить комментарий/фото", reply_markup=markup)
                    if isUser(repliable_id):
                        bot.send_message(repliable_id, 'Ваша заявка выполнена!')
                    else:
                        bot.reply_to(message, "Такой человек к нам не обращался")
            else:
                bot.send_message(message.chat.id, "Введите id")
    else:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'no')
def send_application(call):
    global global_application_number
    if not isDispatcher(call.message.chat.id):
        application_dict[str(call.message.chat.id)]['app_id'] = call.message.chat.id
        application_dict[str(call.message.chat.id)]['app_num'] = global_application_number
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=
        "Ваша заявка отправлена. Чтобы отправить еще одну заявку напишите\n/start")
        if application_dict[str(call.message.chat.id)]['disp_type'] == 'first_disp':
            temp_disp = dispatchers_1
        else:
            temp_disp = dispatchers_2
        for i in range(len(temp_disp)):
            bot.send_message(temp_disp[i],
                             f"Application number: {application_dict[str(call.message.chat.id)]['app_num']}\nApplication id: <code>{application_dict[str(call.message.chat.id)]['app_id']}</code>\nStreet: {application_dict[str(call.message.chat.id)]['street']}\nHouse: {application_dict[str(call.message.chat.id)]['house_num']}\nProblem: {application_dict[str(call.message.chat.id)]['problem']}", parse_mode="html")
        if len(user_photos_dict[str(call.message.chat.id)]) > 0:
            for i in user_photos_dict[str(call.message.chat.id)]:
                for j in range(len(temp_disp)):
                    bot.copy_message(temp_disp[j], call.message.chat.id, i)
        user_photos_dict[str(call.message.chat.id)] = []
        counter_dict[str(call.message.chat.id)] = 0
        global_application_number += 1
        update_global_app_num(global_application_number)
    else:
        global repliable_id
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Ответ по заявке отправлен!")
        if len(dict_disp_photos[str(call.message.chat.id)]) > 0:
            for i in dict_disp_photos[str(call.message.chat.id)]:
                bot.copy_message(repliable_id, call.message.chat.id, i)
        counter_dict[str(call.message.chat.id)] = 10
        repliable_id = ''
        dict_disp_photos[str(call.message.chat.id)] = []


@bot.callback_query_handler(func=lambda call: call.data == 'yes')
def call_foo(call):
    global repliable_id
    if isDispatcher(call.message.chat.id):
        bot.register_next_step_handler(call.message, attach_photo)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Пожалуйста, отправьте фото или комментарий")
        bot.register_next_step_handler(call.message, ask_for_attach)
    else:
        bot.register_next_step_handler(call.message, attach_photo)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text="Пожалуйста, отправьте фото")
        bot.register_next_step_handler(call.message, ask_for_attach)


@bot.message_handler(content_types=['photo'])
def attach_photo(message):
    if isDispatcher(message.chat.id):
        dict_disp_photos[str(message.chat.id)].append(message.id)
    else:
        user_photos_dict[str(message.chat.id)].append(message.id)


def ask_for_attach(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("Да", callback_data='yes')
    btn2 = types.InlineKeyboardButton("Нет", callback_data='no')
    markup.add(btn1, btn2)
    if isDispatcher(message.chat.id):
        bot.send_message(message.chat.id, "Желаете прикрепить ещё фото или комментарий", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Желаете прикрепить еще фото?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'nea')
def ending_disp(call):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text="Ответ по заявке отправлен")


@bot.callback_query_handler(func=lambda call: call.data == 'first_disp')
def to_first(call):
    application_dict[str(call.message.chat.id)]['disp_type'] = call.data
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text='Пожалуйста, внимательно прочтите инструкции для корректного формирования заявки.\n\nНапишите, пожалуйста, <b><u>только</u></b> название вашей улицы.',parse_mode="html")


@bot.callback_query_handler(func=lambda call: call.data == 'second_disp')
def to_second(call):
    application_dict[str(call.message.chat.id)]['disp_type'] = call.data
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                          text='Пожалуйста, внимательно прочтите инструкции для корректного формирования заявки.\n\nНапишите, пожалуйста, <b><u>только</u></b> название вашей улицы.',parse_mode="html")


bot.polling(none_stop=True, interval=0)
