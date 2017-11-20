#coding:utf-8
import telebot
import datetime
import time
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    , level = logging.INFO)

def niceprint(string):
    tabindex = 0
    out = ''
    for i in string:
        if i == ',':
            out += i
            out += '\n'
            out += '\t' * tabindex
            continue
        if i == '{':
            tabindex += 1
        if i == '}':
            tabindex -= 1
            out += '\n'
        out += i
    return out

salfetka = '''
‼️ Режим тишины! ‼️
Ходок! Приготовься к атаке (⚔ Атака) до 'Смелый Вояка, Выбирай врага!'

Если ты вдруг любишь перед боем переодеваться, тебе может помочь пойти и переодеться!

















‼️ Режим тишины! ‼️
 '''

bot = telebot.TeleBot("439405383:AAEuNE8fZegg00zArV1LEFzAyVd-2Sngea0")

while 1:
    now = str(datetime.datetime.now().time().replace(microsecond=0))
    if now in ['03:54:59', '07:54:59', '11:54:59', '15:54:59', '19:54:59', '23:54:59']:
        logging.info('Запуск салфетки по таймеру в:', now)

        msg = bot.send_message(-1001064490030, salfetka)
        bot.pin_chat_message(msg.chat.id, msg.message_id)

        logging.debug(niceprint(str(msg)))
        time.sleep(1)