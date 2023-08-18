import ptbot
import os
import random
from pytimeparse import parse


FIRST_SECRET = os.environ['TOKEN']
SECOND_SECRET = os.environ['TG_CHAT_ID']


def notify_progress(secs_left, second_secret, 
                    message_id, msg):
    progressbar = render_progressbar(msg, secs_left)
    bot.update_message(second_secret, message_id, 
                       "Осталось {} секунд\n{}".format(secs_left, progressbar))
    

def notify():
    bot.send_message(SECOND_SECRET, "Время вышло!")


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


def choose(second_secret, question):
    msg = parse(question)
    message_id = bot.send_message(second_secret, "Запускаю таймер...")
    bot.create_countdown(msg, notify_progress,
                         second_secret=second_secret,
                         message_id=message_id, 
                         msg=msg)
    bot.create_timer(msg, notify)


def main():
    bot.send_message(SECOND_SECRET, "Привет!")
    bot.send_message(SECOND_SECRET, "Запускаю таймер...")
    bot.reply_on_message(choose)
    bot.run_bot() 


if __name__ == "__main__":
    bot = ptbot.Bot(FIRST_SECRET)
    main()


