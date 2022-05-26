import json
import telebot
from telebot import types
import requests
import bs4
import BotGames
from BotMenu import Menu, Users
import DZ
import BotFun
import TTTGame
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

bot = telebot.TeleBot('5193117811:AAH0hWHVx0kH08sub52IFj2SAdJi1eugY-k')
game21 = None
TTT_LOBBY = TTTGame.TTTLobby()

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAIaeWJEeEmCvnsIzz36cM0oHU96QOn7AAJUAANBtVYMarf4xwiNAfojBA")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


# -----------------------------------------------------------------------
# Получение стикеров от юзера
@bot.message_handler(content_types=['sticker'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    sticker = message.sticker
    bot.send_message(message.chat.id, sticker)

    # глубокая инспекция объекта
    # import inspect,pprint
    # i = inspect.getmembers(sticker)
    # pprint.pprint(i)


# -----------------------------------------------------------------------
# Получение аудио от юзера
@bot.message_handler(content_types=['audio'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    audio = message.audio
    bot.send_message(chat_id, audio)

# -----------------------------------------------------------------------
# Получение голосовухи от юзера
@bot.message_handler(content_types=['voice'])
def get_messages(message):
    chat_id = message.chat.id
    result = bot.send_message(chat_id, "Это " + message.content_type)
    print(result)

    voice = message.voice


# -----------------------------------------------------------------------
# Получение фото от юзера
@bot.message_handler(content_types=['photo'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    photo = message.photo
    bot.send_message(message.chat.id, photo)


# -----------------------------------------------------------------------
# Получение видео от юзера
@bot.message_handler(content_types=['video'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    video = message.video
    bot.send_message(message.chat.id, video)


# -----------------------------------------------------------------------
# Получение документов от юзера
@bot.message_handler(content_types=['document'])
def get_messages(message):
    chat_id = message.chat.id
    mime_type = message.document.mime_type
    bot.send_message(chat_id, "Это " + message.content_type + " (" + mime_type + ")")

    document = message.document
    bot.send_message(message.chat.id, document)
    if message.document.mime_type == "video/mp4":
        bot.send_message(message.chat.id, "This is a GIF!")


# -----------------------------------------------------------------------
# Получение координат от юзера
@bot.message_handler(content_types=['location'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    location = message.location
    bot.send_message(message.chat.id, location)


# -----------------------------------------------------------------------
# Получение контактов от юзера
@bot.message_handler(content_types=['contact'])
def get_messages(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Это " + message.content_type)

    contact = message.contact
    bot.send_message(message.chat.id, contact)


# -----------------------------------------------------------------------
# Обработка кнопок TTTGame
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    if call.data.split(":")[0] == "TTT":
        TTT_LOBBY.step(call.data, call.from_user.id, call.id)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    chat_id = message.chat.id
    ms_text = message.text
    update_sheet(message.chat.id, message.text)

    cur_user = Users.getUser(chat_id)
    if cur_user is None:
        cur_user = Users(chat_id, message.json["from"])

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu != None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Играть в крестики-нолики":
            TTT_LOBBY.play(chat_id, message.from_user.username)
            print(message.from_user.username)

        elif ms_text == "Прислать фильм":
            BotFun.send_film(chat_id)

        elif ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=BotFun.get_dogURL(), caption="Вот тебе собачка!")

        elif ms_text == "Прислать случайного пользователя":
            bot.send_photo(chat_id, photo=BotFun.get_randomUserFoto(), caption=BotFun.get_randomUserInfo())

        elif ms_text == "Прислать анекдот c anekdotme.ru":
            bot.send_message(chat_id, text=BotFun.get_anekdot('http://anekdotme.ru/random',  '.anekdot_text'))

        elif ms_text == "Прислать анекдот c nekdo.ru":
            bot.send_message(chat_id, text=BotFun.get_anekdot('https://nekdo.ru/random', '.text'))

        elif ms_text == "Угадай кто?":
            BotGames.get_ManOrNot(chat_id)

        elif ms_text == "Карту!":
            game21 = BotGames.getGame(chat_id)
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=BotGames.getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                BotGames.stopGame(chat_id)
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text in BotGames.GameRPS.values:  # реализация игры Камень-ножницы-бумага
            gameRSP = BotGames.getGame(chat_id)
            if gameRSP is None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return
            text_game = gameRSP.playerChoice(ms_text)
            bot.send_message(chat_id, text=text_game)
            gameRSP.newGame()

        elif ms_text == "Задание-1":
            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание-2":
            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание-3":
            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание-4":
            DZ.dz4(bot, chat_id)

        elif ms_text == "Задание-5":
            DZ.dz5(bot, chat_id)

        elif ms_text == "Задание-6":
            DZ.dz6(bot, chat_id)

    else:  # ...........................................................................................................
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")
# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    pass

# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            game21 = BotGames.newGame(chat_id, BotGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=BotGames.getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Камень, ножницы, бумага":
            gameRSP = BotGames.newGame(chat_id, BotGames.GameRPS())  # создаём новый экземпляр игры
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"
            bot.send_photo(chat_id, photo="https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg", caption=text_game, parse_mode='HTML')

        return True
    else:
        return False


# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Яковлева Вероника")
    key1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/chicanica")
    key1.add(btn1)
    img = open('foto.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=key1)

# ---------------------------------------------------------------------
#Работа с google sheets

CREDENTIALS_FILE = 'pytelebot-21ad3075c3ed.json'    # имя файла с закрытым ключом
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets',
                                                                                  'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

current_date = datetime.now().date()

#Создание нового google-документа с таблицами
spreadsheet = service.spreadsheets().create(body={
    'properties': {'title': 'pytelebot-messages', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': f"{current_date}"}}]
}).execute()
print(spreadsheet)

#настройки доступа к документу для чтения
driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
shareRes = driveService.permissions().create(
    fileId=spreadsheet['spreadsheetId'],
    body={'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
    fields='id'
).execute()

row = 0
def update_sheet(chat_id, message):
    global row
    row += 1

    current_datetime = datetime.now()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheet['spreadsheetId'], body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": f"A{row}:{row}",
             "majorDimension": "ROWS",     # сначала заполнять ряды, затем столбцы (т.е. самые внутренние списки в values - это ряды)
             "values": [[chat_id, f"{current_datetime}", message]],
             }]
    }).execute()

#Документ по адресу https://docs.google.com/spreadsheets/d/spreadsheetId/edit
#spreadsheetId выводится в консоль

# ---------------------------------------------------------------------

bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()