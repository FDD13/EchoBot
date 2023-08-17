import ptbot
import os
import random
from pytimeparse import parse


FIRST_SECRET = os.environ['TOKEN']
SECOND_SECRET = os.environ['TG_CHAT_ID']
BOT = ptbot.Bot(FIRST_SECRET)



def notify_progress(secs_left, second_secret, 
                    message_id, msg):
    progressbar = render_progressbar(msg, secs_left)
    BOT.update_message(second_secret, message_id, 
                       "Осталось {} секунд\n{}".format(secs_left, progressbar))
    

def notify():
    BOT.send_message(SECOND_SECRET, "Время вышло!")


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
    message_id = BOT.send_message(second_secret, "Запускаю таймер...")
    BOT.create_countdown(msg, notify_progress,
                         second_secret=second_secret,
                         message_id=message_id, 
                         msg=msg)
    BOT.create_timer(msg, notify)


def main():
    BOT.send_message(SECOND_SECRET, "Привет!")
    BOT.send_message(SECOND_SECRET, "Запускаю таймер...")
    BOT.reply_on_message(choose)
    BOT.run_bot() 


if __name__ == "__main__":
    main()


