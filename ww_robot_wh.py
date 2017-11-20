#coding:utf-8
import telebot
import inventory
import sqlite3
import logging
import time
import datetime
import config
import flask
from telebot import types

###############################################################
API_TOKEN = config.token
WEBHOOK_HOST = '85.143.174.217'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr
WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % API_TOKEN
# logger = telebot.logger
# telebot.logger.setLevel(logger.info)
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
###############################################################


adminskeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
adminskeyboard.add(*[telebot.types.KeyboardButton(name) for name in ['⚔️Битва', '/getall', '/showall']])

keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['/getme', '/addmetomobs', '/delmefrommobs']])

adminskeyboarhide = telebot.types.ReplyKeyboardRemove()

admins = ['Vozhik', 'belaya_devushka', 'danilsolo', 'MarieKoko', 'Fenicu', 'Wood_elf', 'Puzya']

salfetka = '''
‼️ Режим тишины! ‼️
Ходок! Приготовься к атаке (⚔ Атака) до 'Смелый Вояка, Выбирай врага!'

Если ты вдруг любишь перед боем переодеваться, тебе может помочь пойти и переодеться!

















‼️ Режим тишины! ‼️
 '''

BOTCHAT = 76201733
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s'
                    , level=logging.INFO)

# создаём logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# создаём консольный handler и задаём уровень
ch = logging.FileHandler('ww.log')
ch.setLevel(logging.INFO)

# создаём formatter
formatter = logging.Formatter(u'%(filename)s[LINE:%(lineno)-3s]# %(levelname)-5s [%(asctime)s] %(message)s')

# добавляем formatter в ch
ch.setFormatter(formatter)


# добавляем ch к logger
logger.addHandler(ch)


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


# bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    userid = message.from_user.id
    username = message.from_user.username

    logger.info('user: ' + str(username) + ' command: /start')

    if message.chat.type == 'supergroup':
        return

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()

    userlist = []
    for row in c.execute('select username from profiles'):
        userlist.append(row[0])

    if username in userlist:
        if username in admins:
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы', reply_markup=adminskeyboard)
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы', reply_markup=keyboard)
        conn.commit()
        conn.close()
    else:
        querry = "insert into profiles (id, username) values ('{}', '{}')".format(userid, username)
        logger.debug('new: ' + str(username))
        c.execute(querry)
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, 'Вы зарегистрированы', reply_markup=keyboard)


@bot.message_handler(commands=['getall2'])
def getallusers(message):
    logger.info('user: ' + str(message.from_user.username) + ' command: /getall2')

    if message.from_user.username not in admins:
        return

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    querry = "select * from profiles"
    logger.debug(querry)
    out = ''
    for i in c.execute(querry):
        out += '@' + str(i[1]) + ' | ' + str(i[2]) + ' | ' + str(i[3]) + '\n'
        out += '🏅' + str(i[4]) + ' ⚔' + str(i[5]) + ' 🛡' + str(i[6]) + ' 🔥' + str(i[7]) + ' 🤺' + str(i[12]) + '\n'
        out += '<code>🤛🏻</code>' + str(i[13]) + '\n'
        out += '<code>🤜🏻</code>' + str(i[14]) + '\n'
        out += '<code>🎩</code>' + str(i[15]) + '\n'
        out += '<code>👐🏻</code>' + str(i[16]) + '\n'
        out += '<code>👕</code>' + str(i[17]) + '\n'
        out += '<code>👢</code>' + str(i[18]) + '\n'
        out += '<code>🌂</code>' + str(i[19]) + '\n'
        if str(i[21]) == '':
            out += '🌿\n'
        else:
            out += str(i[21]) + '\n'

        out += '📦' + str(i[20]) + '\n'
        out += '🕐' + str(i[22]) + '\n\n'

    logger.debug(out)
    bot.send_message(message.chat.id, out, parse_mode='HTML', reply_markup=adminskeyboarhide)
    conn.commit()
    conn.close()


@bot.message_handler(commands=['getall'])
def getallusers(message):
    logger.info('user: ' + str(message.from_user.username) + ' command: /getall')

    if message.from_user.username not in admins:
        return

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    querry = "select * from profiles"
    logger.debug(querry)
    out = ''

    for idx, i in enumerate(c.execute(querry)):
        out += '@' + str(i[1]) + ' | ' + str(i[2]) + ' | ' + str(i[3]) + '\n'
        out += '🏅' + str(i[4]) + ' ⚔' + str(i[5]) + ' 🛡' + str(i[6]) + ' 🔥' + str(i[7]) + ' 🤺' + str(i[12]) + '\n'
        out += '🤛🏻' + str(i[13]) + '\n'
        out += '🤜🏻' + str(i[14]) + '\n'
        out += '🎩' + str(i[15]) + '\n'
        out += '👐🏻' + str(i[16]) + '\n'
        out += '👕' + str(i[17]) + '\n'
        out += '👢' + str(i[18]) + '\n'
        out += '🌂' + str(i[19]) + '\n'
        if str(i[21]) == '':
            out += '🌿\n'
        else:
            out += str(i[21]) + '\n'

        out += '📦' + str(i[20]) + '\n'
        out += '🕐' + str(i[22]) + '\n\n'

        if (idx + 1) % 8 == 0:
            bot.send_message(message.chat.id, out, parse_mode='HTML')
            out = ''

    if out != '':
        bot.send_message(message.chat.id, out)
    conn.commit()
    conn.close()


@bot.message_handler(commands=['getme'])
def getme(message):
    logger.info('user: ' + str(message.from_user.username) + ' command: /getme')

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    querry = "select * from profiles where id = {}".format(message.from_user.id)
    logger.debug(querry)
    for i in c.execute(querry):
        logger.debug(str(i))

        out = '@' + str(i[1]) + ' | ' + str(i[2]) + ' | ' + str(i[3]) + '\n'
        out += '🏅' + str(i[4]) + ' ⚔' + str(i[5]) + ' 🛡' + str(i[6]) + ' 🔥' + str(i[7]) + ' 🤺' + str(i[12]) + '\n'
        out += '<code>🤛🏻</code>' + str(i[13]) + '\n'
        out += '<code>🤜🏻</code>' + str(i[14]) + '\n'
        out += '<code>🎩</code>' + str(i[15]) + '\n'
        out += '<code>👐🏻</code>' + str(i[16]) + '\n'
        out += '<code>👕</code>' + str(i[17]) + '\n'
        out += '<code>👢</code>' + str(i[18]) + '\n'
        out += '<code>🌂</code>' + str(i[19]) + '\n'
        out += str(i[21]) + '\n'

        out += '📦' + str(i[20]) + '\n'
        out += '🕐' + str(i[22])[:-7] + '\n'

        bot.send_message(message.chat.id, out,  parse_mode='HTML')
        # bot.send_message(message.chat.id, str(i))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['del'])
def delusers(message):
    logger.info('user: ' + str(message.from_user.username) + ' command: /del')
    logger.debug(str(message.text).split())

    if message.from_user.username not in admins:
        return

    try:
        str(message.text).split()[1]
    except IndexError:
        bot.send_message(message.chat.id, 'Укажи имя кого турнуть')
        return
    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    querry = "select username from profiles where username = '{}'".format(str(message.text).split()[1])
    logger.debug(querry)
    for i in c.execute(querry):
        logger.debug('aaa' + str(i))
        querry = "delete from profiles where username = '{}'".format(str(message.text).split()[1])
        logger.debug(querry)

        for j in c.execute(querry):
            logger.debug(j)

    conn.commit()
    conn.close()


@bot.message_handler(commands=['delall'])
def delallusers(message):
    logger.info('user: ' + str(message.from_user.username) + ' command: /dellall')

    if message.from_user.username not in admins:
        return

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    querry = "delete from profiles"
    logger.debug(querry)
    for i in c.execute(querry):
        logger.debug(str(i))
        bot.send_message(message.chat.id, str(i))
    conn.commit()
    conn.close()


@bot.message_handler(commands=['showall'])
def showallusers(message):
    # logger.debug()(niceprint(str(message)))
    logger.info('user: ' + str(message.from_user.username) + ' command: /showall')

    if message.from_user.username not in admins:
        return
    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    querry = "select * from profiles order by attack"
    logger.debug(querry)
    out = ''

    for idx, i in enumerate(c.execute(querry)):
        out += str(i[2]) + '|'
        out += '🏅' + str(i[4]) + ' ⚔' + str(i[5]) + ' 🛡' + str(i[6]) + '|' + str(i[3])[0] + '\n'
        out += '/show_' + str(i[1]) + '\n\n'

    bot.send_message(message.chat.id, out)
    conn.commit()
    conn.close()

@bot.message_handler(commands=['addmetomobs'])
def addmetomobs(message):

    logger.info('user: ' + str(message.from_user.username) + ' command: /addmetomobs')

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()

    for i in c.execute('select username from mobspersons'):
        if message.from_user.username == i[0]:
            bot.reply_to(message, 'Вы уже зарегистрированы')
            return

    querry = "insert into mobspersons values('{}')".format(message.from_user.username)
    c.execute(querry)
    logger.debug(querry)

    bot.reply_to(message, 'Вы добавлены на мобов')
    conn.commit()
    conn.close()

@bot.message_handler(commands=['delmefrommobs'])
def delmetomobs(message):

    logger.info('user: ' + str(message.from_user.username) + ' command: /delmefrommobs')

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()

    querry = "delete from mobspersons where username = ('{}')".format(message.from_user.username)
    c.execute(querry)
    logger.debug(querry)

    bot.reply_to(message, 'Вы удалены с мобов')
    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: message.text and '/show' in message.text, content_types=['text'])
def getcurrentuser(message):
    logger.debug(niceprint(str(message)))
    logger.info('user: ' + str(message.from_user.username) + ' command: ' + message.text)

    if message.from_user.username not in admins:
        return

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()
    end = None if message.text.find('@') == -1 else message.text.find('@')
    logger.debug(message.text[6:message.text.find('@')])
    querry = "select * from profiles where username = '{}'".format(message.text[6:end])
    logger.debug(querry)
    for i in c.execute(querry):
        logger.debug(str(i))

        out = '@' + str(i[1]) + ' | ' + str(i[2]) + ' | ' + str(i[3]) + '\n'
        out += '🏅' + str(i[4]) + ' ⚔' + str(i[5]) + ' 🛡' + str(i[6]) + ' 🔥' + str(i[7]) + ' 🤺' + str(i[12]) + '\n'
        out += '<code>🤛🏻</code>' + str(i[13]) + '\n'
        out += '<code>🤜🏻</code>' + str(i[14]) + '\n'
        out += '<code>🎩</code>' + str(i[15]) + '\n'
        out += '<code>👐🏻</code>' + str(i[16]) + '\n'
        out += '<code>👕</code>' + str(i[17]) + '\n'
        out += '<code>👢</code>' + str(i[18]) + '\n'
        out += '<code>🌂</code>' + str(i[19]) + '\n'
        out += str(i[21]) + '\n'

        out += '📦' + str(i[20]) + '\n'
        out += '🕐' + str(i[22])[:-7] + '\n'

        logger.debug(out)
        bot.send_message(message.chat.id, out, parse_mode='HTML')
        # bot.send_message(message.chat.id, str(i))
    conn.commit()
    conn.close()

@bot.message_handler(func=lambda message: message.text and message.chat.type == 'private', content_types=['text'])
def getprofile(message):
    # logger.debug()(niceprint(str(message)))
    # logger.debug()(time.time())
    # print(str(message.from_user.username) + ': ' + message.text)
    # print(message.text.split('\n'))

    logger.info('user: ' + str(message.from_user.username) + ': ' + str(message.text))


    userid = message.from_user.id
    username = message.from_user.username

    conn = sqlite3.connect('wwbot.db')
    c = conn.cursor()

    userlist = []
    for row in c.execute('select username from profiles'):
        userlist.append(row[0])
    conn.commit()
    conn.close()

    if '/class' in message.text \
            and '🇨🇾' in message.text \
            and message.forward_from.id == 265204902 \
            and username in userlist:  # and message.forward_date > time.time() - 60:

        logger.info('пользователь: ' + str(message.from_user.username) + ' прислал профиль')
        # niceprint(message.text)

        heroinfo = message.text.split('\n')
        herosword = ''
        herosdagger = ''
        herohead = ''
        heroarms = ''
        herobody = ''
        herolegs = ''
        herospecials = ''
        pet = ''

        for param in heroinfo:
            # logger.debug()(param)
            if param[0:2] in ['🇨🇾', '🇬🇵', '🇪🇺', '🇮🇲', '🇻🇦', '🇲🇴', '🇰🇮']:
                heroflag = param[:2]
                heroname = param[2:param.find(',')]
                heroprof = param[param.find(',')+1:].split()[0]
                logger.debug('heroflag: ' + heroflag)
                logger.debug('heroname: ' + str(heroname))
                logger.debug('hero prof: ' + str(heroprof))

            if param[0:2] == '🏅У':
                herolevel = param.split()[1]
                logger.debug('hero level: ' + str(herolevel))

            if param[0:1] == '⚔':
                heroattack = param.split()[1]
                herodefense = param.split()[3]
                logger.debug('hero attack: ' + str(heroattack))
                logger.debug('hero defense: ' + str(herodefense))

            if param[0:1] == '🔥':
                heroexp = param.split()[1].split('/')[0]
                logger.debug('hero exp: ' + str(heroexp))

            if param[0:1] == '🔋':
                herostamina = param.split()[1].split('/')[0]
                logger.debug('hero stamina: ' + str(herostamina))

            heromana = 0
            if param[0:1] == '💧':
                heromana = param.split()[1].split('/')[0]
                logger.debug('mana: ' + str(heromana))

            if param[0:1] == '💰':
                herogold = param.split()[0][1:]
                herogems = param.split()[1][1:]
                logger.debug('hero gold: ' + str(herogold))
                logger.debug('hero gems: ' + str(herogems))

            if param[0:1] == '🤺':
                herowins = param.split()[1]
                logger.debug('hero wins: ' + str(herowins))

            if param in inventory.swords:
                herosword = str(param)
                logger.debug('sword: ' + str(herosword))

            if param in inventory.dagger:
                herosdagger = str(param)
                logger.debug('dagger: ' + str(herosdagger))

            if param in inventory.head:
                herohead = str(param)
                logger.debug('head: ' + str(herohead))

            if param in inventory.arms:
                heroarms = str(param)
                logger.debug('arms: ' + str(heroarms))

            if param in inventory.body:
                herobody = str(param)
                logger.debug('body: ' + str(herobody))

            if param in inventory.legs:
                herolegs = str(param)
                logger.debug('legs: ' + str(herolegs))

            if param in inventory.specials:
                herospecials = str(param)
                logger.debug('specials: ' + str(herospecials))

            if param[0:1] == '📦':
                herostock = param.split()[1]
                logger.debug('hero stock: ' + str(herostock))

            if param[0:2] in inventory.pets:
                pet = param
                logger.debug('pet: ' + str(pet))

        querry ='''update profiles
        set heroflag = '{1}',
            heroname = '{2}',
            prof = '{3}',
            attack = '{4}',
            defense = '{5}',
            exp = '{6}',
            stamina = '{7}',
            mana = '{8}',
            gold = '{9}',
            gems = '{10}',
            wins = '{11}',
            sword = '{12}',
            dagger = '{13}',
            head = '{14}',
            arms = '{15}',
            body = '{16}',
            legs = '{17}',
            specials = '{18}',
            stock = '{19}',
            pet = '{20}',
            proftime = '{22}'
        where id = {21}
        '''.format(heroflag, heroname, heroprof, herolevel, heroattack, herodefense, heroexp, herostamina, heromana,
                   herogold, herogems, herowins, herosword, herosdagger, herohead, heroarms, herobody, herolegs,
                   herospecials, herostock, pet, userid, datetime.datetime.now())


        conn = sqlite3.connect('wwbot.db')
        c = conn.cursor()
        logger.debug(querry)
        c.execute(querry)
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, 'Профиль обновлен')

    else:
        logger.info('пользователь: ' + str(message.from_user.username) + ' прислал дерьмовый профиль')
        logger.debug(niceprint(str(message)))
        if username in userlist:
            bot.send_message(message.from_user.id, 'Ты отсылаешь мне какую-то дичь')
        else:
            bot.send_message(message.from_user.id, 'Ты отсылаешь мне какую-то дичь попробуй написать /start')


@bot.message_handler(func=lambda message: message.text and True, content_types=['text'])
def echo_all(message):
    logger.debug(niceprint(str(message)))
    logger.info(str(message.from_user.username) + ': ' + message.text)

    if datetime.datetime.fromtimestamp(message.date) < datetime.datetime.now()-datetime.timedelta(minutes=1):
        logger.info('старое сообщение')
        return

    if 'Ты встретил' in message.text and message.forward_from:
        out = 'Напиши первым любое сообщение реплаем на это и забирай моба, если ты не успел, '
        out += 'попробуй еще раз\nСуммонятся:\n'
        conn = sqlite3.connect('wwbot.db')
        c = conn.cursor()

        for row in c.execute('select username from mobspersons'):
            out += '@' + str(row[0]) + ' '

        conn.commit()
        conn.close()
        bot.reply_to(message, out)

    if 'хомяк' in message.text.lower():
        bot.reply_to(message, '@Hedina69 тут это, по твою душу')

    if 'мясо' in message.text.lower():
        bot.reply_to(message, '@Fenicu тут это, по твою душу')

    if 'пес' in message.text.lower():
        bot.reply_to(message, '@eegor7 тут это, по твою душу')

    if 'Лича (50 ур).' in message.text:
        bot.reply_to(message, 'https://t.me/whitr_lich')

    if 'Черную Бороду (40 ур)' in message.text:
        bot.reply_to(message, 'https://t.me/whiteboroda')

    if 'оксан' in message.text.lower():
        bot.reply_to(message, 'Теперь и я знаю как зовут хедину')

    # if 'бан' in message.text.lower():
    #     bot.reply_to(message, '@denishus тут это, по твою душу')

    if 'корм' in message.text.lower():
        bot.reply_to(message, '@Sicdez тут это, по твою душу')

    if 'режим тишины' in message.text.lower() or 'салфетка' in message.text.lower():
        bot.reply_to(message, salfetka)
        bot.pin_chat_message(-1001064490030, message.message_id + 1)

    if 'пин' in message.text and message.reply_to_message and message.from_user.username in admins:
        bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)


###############################################################
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
time.sleep(1)


# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))


# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)