import json
import telebot
from telebot import types
import requests
import bs4
import BotGames
from BotMenu import Menu
import DZ
import BotFun

bot = telebot.TeleBot('5193117811:AAH0hWHVx0kH08sub52IFj2SAdJi1eugY-k')
game21 = None

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global game21

    chat_id = message.chat.id
    ms_text = message.text

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    if Menu.cur_menu != None and ms_text in Menu.cur_menu.buttons: # проверим, что команда относится к текущему меню

        if ms_text == "Помощь":
            send_help(chat_id)

        elif ms_text == "Прислать фильм":
            send_film(chat_id)

        elif ms_text == "Прислать собаку":
            bot.send_photo(chat_id, photo=BotFun.get_dogURL(), caption="Вот тебе собачка!")

        elif ms_text == "Прислать случайного пользователя":
            bot.send_photo(chat_id, photo=BotFun.get_randomUserFoto(), caption=BotFun.get_randomUserInfo())

        elif ms_text == "Прислать анекдот c anekdotme.ru":
            bot.send_message(chat_id, text=BotFun.get_anekdot('http://anekdotme.ru/random',  '.anekdot_text'))

        elif ms_text == "Прислать анекдот c nekdo.ru":
            bot.send_message(chat_id, text=BotFun.get_anekdot('https://nekdo.ru/random', '.text'))

        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)

        elif ms_text == "Карту!":

            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return

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
#@bot.callback_query_handler(func=lambda call:True)
#def callback_worker(call):






# -----------------------------------------------------------------------

def goto_menu(chat_id, name_menu):

    # получение нужного элемента меню
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            global game21
            game21 = BotGames.Game21()  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        return True
    else:
        return False
# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias

# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Автор: Яковлева Вероника")
    key1 = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Напишите автору", url="https://t.me/chicanica")
    key1.add(btn1)
    img = open('foto.jpg', 'rb')
    bot.send_photo(chat_id, img, reply_markup=key1)

# -----------------------------------------------------------------------
def get_ManOrNot(chat_id):
    global bot
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить", url=" https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)
    req = requests.get(" https://thispersondoesnotexist.com/image ", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Это человек реален?")


# -----------------------------------------------------------------------
def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}\n"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)

# -----------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find("div", align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()
    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]
    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm

# ---------------------------------------------------------------------
bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()