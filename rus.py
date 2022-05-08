import speech_recognition as sr
import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup # Модуль для работы с HTML

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'ru')

def talk(text):
    engine.say(text)
    print(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            talk('слушаю...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
    except:
        pass
    return command
# создать команду, где она будет перечислять все, что она умеет
def assistant():
    command = take_command()
    print(command)

    if 'как тебя зовут' in command:
        talk('--Меня зовут Сандра, я ваш голосовой ассистент--')

    elif 'что ты умеешь?' in command:
        talk('--Вы можете спросить меня о дате, времени, погоде, обменном курсе или просто поговорить со мной--')

    elif 'время' or 'сколько сейчас времени' or 'который час' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'--Время сейчас {time}--')

    elif 'дата' or 'какое сегодня число' in command:
        talk(f"--Today is {datetime.date.today().strftime('%d %B %Y')}--")

    elif 'ты свободна?' or 'мы можем познакомиться?' in command:
        talk('--I am in a relationship with wifi--')

    elif 'курс валют' in command:
        talk('Задайте вопрос в формате "доллар к рублю"')
        query = take_command()
        try:
            query = query.replace(' ', '+')
            URL = f"https://google.com/search?q={query}"
            headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
            full_page = requests.get(URL, headers=headers)
            # Разбираем через BeautifulSoup
            soup = BeautifulSoup(full_page.content, 'html.parser')
            # Получаем нужное для нас значение и возвращаем его
            convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
            currency = convert[0].text
            talk("1 доллар = " + str(currency))
# вариант: ассистентка сразу спрашивает доллар к рублю? евро? и тд
        except Exception as e:
            print("Exception (exchange rate):", e)
            pass

    elif 'погода' in command:
        talk('В каком городе?')
        city = take_command()
        try:
            appid = 'e077f3384632aa771cfdfd210e7a5576'
            url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
            res = requests.get(url.format(city)).json()
            information = {
                'city': city,
                'temperature': res["main"]["temp"]
            }
            talk(f"In {information['city']} {information['temperature']} degrees Celsius")
        except Exception as e:
            print("Exception (weather):", e)
            pass
    else:
        talk('пожалуйста, повторите еще раз')
        return take_command

while True:
    assistant()
