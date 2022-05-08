import speech_recognition as sr
import pyttsx3
import datetime
import requests
from bs4 import BeautifulSoup

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    print(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            talk('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
    except:
        pass
    return command

def assistant():
    command = take_command()
    print(command)

    if 'how is your name' in command:
        talk('I am Sandra, your voice assistant')

    elif 'what can you do' or 'your commands' in command:
        talk('You can ask me about the date, time, weather, exchange rate or just talk with me')

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')

    elif 'date' in command:
        talk(f"Today is {datetime.date.today().strftime('%d %B %Y')}")

    elif 'are you single' in command:
        talk('--I am in a relationship with wifi--')

    elif 'exchange rate' in command:
        talk('Say a request in the format dollar to ruble')
        query = take_command()
        try:
            query = query.replace(' ', '+')
            URL = f"https://google.com/search?q={query}"

            headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

            full_page = requests.get(URL, headers=headers)
            # Разбираем через BeautifulSoup
            soup = BeautifulSoup(full_page.content, 'html.parser')
            # Получаем значение и возвращаем его
            convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
            currency = convert[0].text
            talk("1 dollar is = " + str(currency))
        except Exception as e:
            print("Exception (exchange rate):", e)

    elif 'weather' in command:
        talk('Say only name of city')
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
            print(f"In {information['city']} {information['temperature']} degrees Celsius")

        except Exception as e:
            print("Exception (weather):", e)
            pass
    else:
        talk('please say the command again')
        return take_command
