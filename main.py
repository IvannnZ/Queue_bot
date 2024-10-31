import telebot
import config
import queue_for_bot
from collections import defaultdict

#TODO add git
#TODO add remove queue
#TODO add look queue
#TODO rename queue_to_bot

API_TOKEN = config.TOKEN
bot = telebot.TeleBot(API_TOKEN)

queues = defaultdict(list)
queue_admins = {}


@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Создать очередь', 'Встать в очередь')
    bot.send_message(message.chat.id, "Привет! Что хочешь сделать?", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Создать очередь')
def create_queue(message):
    queue_id = len(queues) + 1
    queues[queue_id].append(message.from_user.id)
    queue_admins[queue_id] = message.from_user.id
    bot.send_message(message.chat.id, f"Очередь #{queue_id} создана. Ты администратор этой очереди.")


# Присоединение к очереди
@bot.message_handler(func=lambda message: message.text == 'Встать в очередь')
def join_queue_request(message):
    if not queues:
        bot.send_message(message.chat.id, "На данный момент нет активных очередей.")
    else:
        queue_list = "\n".join([f"#{queue_id}" for queue_id in queues])
        msg = bot.send_message(message.chat.id, f"Выберите очередь, отправив её номер:\n{queue_list}")
        bot.register_next_step_handler(msg, join_queue)


def join_queue(message):
    try:
        queue_id = int(message.text)
        if queue_id in queues:
            if message.from_user.id not in queues[queue_id]:
                queues[queue_id].append(message.from_user.id)
                bot.send_message(message.chat.id, f"Ты добавлен в очередь #{queue_id}. Ожидай своей очереди.")
            else:
                bot.send_message(message.chat.id, "Ты уже в этой очереди.")
        else:
            bot.send_message(message.chat.id, "Очередь с таким номером не найдена.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, отправь номер очереди.")


@bot.message_handler(commands=['my_position'])
def my_position(message):
    position = None
    for queue_id, queue in queues.items():
        if message.from_user.id in queue:
            position = queue.index(message.from_user.id) + 1
            bot.send_message(message.chat.id, f"Ты находишься на {position} месте в очереди #{queue_id}.")
            break
    if position is None:
        bot.send_message(message.chat.id, "Ты не стоишь ни в одной из очередей.")


@bot.message_handler(commands=['next'])
def next_in_queue(message):
    admin_queues = [qid for qid, admin_id in queue_admins.items() if admin_id == message.from_user.id]
    if not admin_queues:
        bot.send_message(message.chat.id, "Ты не администратор ни одной очереди.")
    else:
        for queue_id in admin_queues:
            if len(queues[queue_id]) > 1:
                next_user = queues[queue_id].pop(1)  # Убираем следующего и оповещаем
                bot.send_message(next_user, "Ты следующий в очереди!")

                # Оповещение следующего за ним участника
                if len(queues[queue_id]) > 2:
                    upcoming_user = queues[queue_id][1]
                    bot.send_message(upcoming_user, "Ты на подходе, будь готов.")
            else:
                bot.send_message(message.chat.id, f"В очереди #{queue_id} нет больше участников.")


bot.polling(none_stop=True)
