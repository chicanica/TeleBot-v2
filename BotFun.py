import requests
import bs4
import telebot
from telebot import types

bot = telebot.TeleBot('5193117811:AAH0hWHVx0kH08sub52IFj2SAdJi1eugY-k')


# -----------------------------------------------------------------------
def get_anekdot(link, className):
    array_anekdots = []
    req_anek = requests.get(link)
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select(className)
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]

# -----------------------------------------------------------------------
def get_dogURL():
    contents = requests.get('https://random.dog/woof.json').json()
    return contents['url']

# -----------------------------------------------------------------------
def get_randomUserInfo():
    contents = requests.get('https://randomuser.me/api/').json()
    name = contents['results'][0]['name']['title'] + ' ' + contents['results'][0]['name']['first'] + ' ' + contents['results'][0]['name']['last']
    age = contents['results'][0]['dob']['age']
    place = contents['results'][0]['location']['timezone']['description']
    place = place.split(',')[0]
    info = name + ', ' + str(age) + '\n' + place
    return info
# -----------------------------------------------------------------------
def get_randomUserFoto():
    contents = requests.get('https://randomuser.me/api/').json()
    foto = contents['results'][0]['picture']['large']
    return foto

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