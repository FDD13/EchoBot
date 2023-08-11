import ptbot
import os
import random
from pytimeparse import parse


my_secret = os.environ['TOKEN']
TG_CHAT_ID = '39444986'
bot = ptbot.Bot(my_secret)
bot.send_message(TG_CHAT_ID, "Привет!")
bot.send_message(TG_CHAT_ID, "Запускаю таймер...")


def notify_progress(secs_left, TG_CHAT_ID, 
                    message_id, msg):
    progressbar = render_progressbar(msg, secs_left)
    bot.update_message(TG_CHAT_ID, message_id, 
                       "Осталось {} секунд\n{}".format(secs_left, progressbar))
    

def notify():
    bot.send_message(TG_CHAT_ID, "Время вышло!")


def render_progressbar(msg, secs_left, 
                       prefix='', suffix='', 
                       length=30, fill='█', 
                       zfill='░'):
    iteration = min(msg, secs_left)
    percent = "{0:.1f}"
    percent = percent.format(100 * (secs_left / float(msg)))
    filled_length = int(length * secs_left // msg)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def choose(chat_id, question):
    msg = parse(question)
    message_id = bot.send_message(TG_CHAT_ID, "Запускаю таймер...")
    bot.create_countdown(msg, notify_progress,
                         TG_CHAT_ID=TG_CHAT_ID,
                         message_id=message_id, 
                         msg=msg)
    bot.create_timer(msg, notify)
    print("Мне написал пользователь с ID:", chat_id)
    print("Он спрашивал:", question)
    print("Я ответил:", question)


def main():
    bot.reply_on_message(choose)
    bot.run_bot() 


if __name__ == "__main__":
    main()


