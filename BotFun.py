import requests
import bs4

# -----------------------------------------------------------------------
def get_anekdot(link, className):
    array_anekdots = []
    req_anek = requests.get(link)
    soup = bs4.BeautifulSoup(req_anek.text, "html.parser")
    result_find = soup.select(className)
    for result in result_find:
        array_anekdots.append(result.getText().strip())
    return array_anekdots[0]

def get_dogURL():
    contents = requests.get('https://random.dog/woof.json').json()
    return contents['url']

def get_randomUserInfo():
    contents = requests.get('https://randomuser.me/api/').json()
    name = contents['results'][0]['name']['title'] + ' ' + contents['results'][0]['name']['first'] + ' ' + contents['results'][0]['name']['last']
    age = contents['results'][0]['dob']['age']
    place = contents['results'][0]['location']['timezone']['description']
    place = place.split(',')[0]
    info = name + ', ' + str(age) + '\n' + place
    return info

def get_randomUserFoto():
    contents = requests.get('https://randomuser.me/api/').json()
    foto = contents['results'][0]['picture']['large']
    return foto