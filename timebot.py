#coding:utf-8
import telebot
import datetime
import time
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    ,level = logging.INFO, filename='ww.log')

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
        logging.info('Запуск салфетки по таймеру в:' + now)

        bot.send_message(-1001064490030, 'СКОРО БИТВА @lolinyan @f0xpwnz @pongg8 @Sicdez @danilsolo')
        bot.send_message(-1001064490030, 'СКОРО БИТВА @Lybot0 @mperrrsh @nii_batca @Puzya @Wood_elf')
        bot.send_message(-1001064490030, 'СКОРО БИТВА @klim9379992 @mirotvArec @FoolishDreamer @nitroacid @TrentorEx')
        bot.send_message(-1001064490030, 'СКОРО БИТВА @Fenicu @SYMRAK @komakomakoma @eegor7 @SenyaArt')
        bot.send_message(-1001064490030, 'СКОРО БИТВА @Irrissa @bigup_universe @Sympho @baka_bunny @Dinker9')
        bot.send_message(-1001064490030, 'СКОРО БИТВА @DiKill @l2aggron @anoouse')

        msg = bot.send_message(-1001064490030, salfetka)
        bot.pin_chat_message(msg.chat.id, msg.message_id)

        logging.debug(niceprint(str(msg)))

    if now in ['03:58:30', '07:58:30', '11:58:30', '15:58:30', '19:58:30', '23:58:30']:
        logging.info('Запуск салфетки по таймеру в:' + now)

        bot.send_message(-1001064490030, 'БИТВА @lolinyan @f0xpwnz @pongg8 @Sicdez @danilsolo')
        bot.send_message(-1001064490030, 'БИТВА @Lybot0 @mperrrsh @nii_batca @Puzya @Wood_elf')
        bot.send_message(-1001064490030, 'БИТВА @klim9379992 @mirotvArec @FoolishDreamer @nitroacid @TrentorEx')
        bot.send_message(-1001064490030, 'БИТВА @Fenicu @SYMRAK @komakomakoma @eegor7 @SenyaArt')
        bot.send_message(-1001064490030, 'БИТВА @Irrissa @bigup_universe @Sympho @baka_bunny @Dinker9')
        bot.send_message(-1001064490030, 'БИТВА @DiKill @l2aggron @anoouse')

    if now in ['03:31:59', '07:31:59', '11:31:59', '15:31:59', '19:31:59', '23:31:59']:
        logging.info('Запуск салфетки по таймеру в:' + now)

        bot.send_message(-1001064490030, 'Ткни плюс @lolinyan @f0xpwnz @pongg8 @Sicdez @danilsolo')
        bot.send_message(-1001064490030, 'Ткни плюс @Lybot0 @mperrrsh @nii_batca @Puzya @Wood_elf')
        bot.send_message(-1001064490030, 'Ткни плюс @klim9379992 @mirotvArec @FoolishDreamer @nitroacid @TrentorEx')
        bot.send_message(-1001064490030, 'Ткни плюс @Fenicu @SYMRAK @komakomakoma @eegor7 @SenyaArt')
        bot.send_message(-1001064490030, 'Ткни плюс @Irrissa @bigup_universe @Sympho @baka_bunny @Dinker9')
        bot.send_message(-1001064490030, 'Ткни плюс @DiKill @l2aggron @anoouse')


    time.sleep(1)
