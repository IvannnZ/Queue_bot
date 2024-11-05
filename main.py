import telebot
import config
from collections import defaultdict

from queue_for_bot import Admin
from queue_for_bot import User

# TODO add git
# TODO add remove queue
# TODO add look queue
# TODO rename queue_to_bot

API_TOKEN = config.TOKEN
bot = telebot.TeleBot(API_TOKEN)

Admins = {}
Users = {}

markup_Create_Get_in = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_Create_Get_in.row('Создать очередь', 'Встать в очередь')

markup_Get_in = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_Get_in.row('Встать в очередь')

markup_empty = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

markup_FULL_Admin = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_FULL_Admin.row('Создать очередь', 'Встать в очередь', 'следующий', 'посмотреть где я')

markup_FULL_User = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_FULL_User.row('Создать очередь', 'Встать в очередь', 'посмотреть где я')


def send_User_or_Admin(id_User_or_Admin, text):
    if id_User_or_Admin in Admins:
        msg = bot.send_message(id_User_or_Admin, text, reply_markup=markup_FULL_Admin)
    else:
        msg = bot.send_message(id_User_or_Admin, text, reply_markup=markup_FULL_User)
    return msg


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Что хочешь сделать?", reply_markup=markup_FULL_User)


@bot.message_handler(func=lambda message: message.text == 'Создать очередь')
def create_queue(message):
    for i in Admins:
        if Admins[i].id_Admin == message.chat.id:
            bot.send_message(message.chat.id, "Вы уже админ очереди, вы можете быть админом только 1 очереди",
                             reply_markup=markup_FULL_Admin)
    msg = bot.send_message(message.chat.id, "Введи своё имя", reply_markup=markup_empty)
    bot.register_next_step_handler(msg, create_queue1)


def create_queue1(message):
    Admins[message.chat.id] = Admin(message.chat.id, message.text)
    Users[message.chat.id] = User(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Отлично, очередь создана\nP.s. ты в ней не стоишь, встань в неё сам",
                     reply_markup=markup_FULL_Admin)


@bot.message_handler(func=lambda message: message.text == 'Встать в очередь')
def join_queue_request(message):
    if not Admins:
        bot.send_message(message.chat.id, "На данный момент нет активных очередей.\nВы можете создать её",
                         reply_markup=markup_FULL_User)
    else:
        if message.chat.id in Users:
            queue_list_l = list()
            for i in Admins:
                queue_list_l.append(Admins[i].name)
            queue_list = "\n".join([f"#{i} :{queue_list_l[i]}" for i in range(len(queue_list_l))])
            msg = bot.send_message(message.chat.id, f"Выберите очередь, отправив её номер:\n{queue_list}",
                                   reply_markup=markup_empty)
            bot.register_next_step_handler(msg, join_queue)
        else:
            msg = bot.send_message(message.chat.id, "Введи своё имя", reply_markup=markup_empty)
            bot.register_next_step_handler(msg, create_user)


def create_user(message):
    Users[message.chat.id] = User(message.chat.id, message.text)
    queue_list_l = list()
    for i in Admins:
        queue_list_l.append(Admins[i].name)
    queue_list = "\n".join([f"#{i} :{queue_list_l[i]}" for i in range(len(queue_list_l))])

    msg = bot.send_message(message.chat.id, f"Выберите очередь, отправив её номер:\n{queue_list}",
                           reply_markup=markup_empty)
    bot.register_next_step_handler(msg, join_queue)


def join_queue(message):
    try:
        queue_id = int(message.text)
        if queue_id < len(Admins):
            admin_num = 0
            for i in Admins:
                if queue_id == 0:
                    admin_num = i
                    break
                queue_id -= 1
            if message.from_user.id not in Admins[admin_num]:
                Admins[admin_num].add_user(Users[message.chat.id])

                send_User_or_Admin(message.chat.id, f"Ты добавлен в очередь #{queue_id}. Ожидай своей очереди.")
            else:
                send_User_or_Admin(message.chat.id, "Ты уже в этой очереди.")
        else:
            send_User_or_Admin(message.chat.id, "Очередь с таким номером не найдена.")
    except ValueError:
        queue_list_l = list()
        for i in Admins:
            queue_list_l.append(Admins[i].name)
        queue_list = "\n".join([f"#{i} :{queue_list_l[i]}" for i in range(len(queue_list_l))])

        msg = bot.send_message(message.chat.id, f"Пожалуйста, отправь номер очереди.\n{queue_list}",
                               reply_markup=markup_empty)
        bot.register_next_step_handler(msg, join_queue)


@bot.message_handler(func=lambda message: message.text == 'посмотреть где я')
def my_position(message):
    answ_l = []
    for i in Admins:
        pos = Admins[i].admin_queue.search_by_id(message.chat.id)
        if pos is not None:
            answ_l.append((Admins[i].name, pos))
    if answ_l:
        answ = "\n".join(f"Ты находишься на {poss} месте в очереди {name}" for name, poss in answ_l)
        send_User_or_Admin(message.chat.id, answ)
    else:
        send_User_or_Admin(message.chat.id, "Ты не стоишь ни в одной из очередей.")


@bot.message_handler(func=lambda message: message.text == 'следующий')
def next_in_queue(message):
    if message.chat.id in Admins:
        now, next = Admins[message.chat.id].next_in_queue()
        if now is None:
            del Admins[message.chat.id]
            bot.send_message(message.chat.id, "И так, поздравляю, больше нет людей в очереди",
                             reply_markup=markup_FULL_User)
            return
        elif next is None:
            send_User_or_Admin(now.id_User,
                               f"Ты сейчас сдаёшь, подойди для сдачи в очередь: {Admins[message.chat.id].name}")
            del Admins[message.chat.id]
            bot.send_message(message.chat.id,
                             "И так, поздравляю, это последний человек в очереди, но пользователи всё ещё могут добавиться",
                             reply_markup=markup_FULL_User)
            return
        else:
            send_User_or_Admin(now.id_User,
                               f"Ты сейчас сдаёшь, подойди для сдачи в очередь: {Admins[message.chat.id].name}")
            send_User_or_Admin(next.id_User,
                               f"Ты сейчас сдаёшь следующим, подойди для сдачи в очередь: {Admins[message.chat.id].name}")
            send_User_or_Admin(message.chat.id,
                               f"Сейчас сдаёт: {now.name}\nследующий: {next.name}\nвсего в очереди: {Admins[message.chat.id].lenght()}")
            return
    else:
        bot.send_message(message.chat.id,
                         "ЙООООу, так, либо ты сломал бота, либо у меня что-то не так, так или иначе напиши мне @Not_IvannZ")
        return


bot.polling(none_stop=True)
