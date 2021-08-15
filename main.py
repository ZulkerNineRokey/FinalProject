import pyttsx3
import datetime
import speech_recognition as sr
import subprocess
import wikipedia
import os
import sys
import calendar
import pyowm
import pywhatkit
import requests
from bs4 import BeautifulSoup

# voice, rate, volume
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # voice ,index 0 for male & 1 for female
engine.setProperty('rate', 175)  # setting up new voice rate
engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1


# Speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Greeting
def greeting():
    """
    From  -  To  => part of day
        ---------------------------
        00:00 - 04:59 => midnight
        05:00 - 06:59 => dawn
        07:00 - 10:59 => morning
        11:00 - 12:59 => noon
        13:00 - 16:59 => afternoon
        17:00 - 18:59 => dusk
        19:00 - 20:59 => evening
        21:00 - 23:59 => night
    """
    hour = datetime.datetime.now().hour
    if 0 <= hour < 5:
        speak('Good midnight!')
    elif 5 <= hour < 7:
        speak('Good dawn!')
    elif 7 <= hour < 11:
        speak('Good morning!')
    elif 11 <= hour < 13:
        speak('Good noon!')
    elif 13 <= hour < 17:
        speak('Good afternoon!')
    elif 17 <= hour < 19:
        speak('Good dusk')
    elif 19 <= hour < 21:
        speak('Good evening!')
    else:
        speak('Good night!')
    speak('How are you?')


# Take commands
def take_command():
    """
    It take microphone input from the user.
    return : string output
    """

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening ...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing ...")
        query = r.recognize_google(audio, language="en")
        print(f"User said : {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again, please ...")
        return "NONE"
    return query


if __name__ == "__main__":
    speak('hello')
    greeting()
    while True:
        _query = take_command().lower()
        # Logic for executing tasks based on _query

        # Basic Conversation
        if 'how are you' in _query:
            speak('I am fine ,thank you')
            speak("And you?")

        elif 'and you' in _query:
            speak('I am also fine thank you.')
            speak('How may i help you')

        elif 'thank you' in _query:
            speak('Welcome sir')
            speak('How may I help you?')

        # System Related Command:
        elif 'exit' in _query:
            sys.exit()

        elif 'open task manager' in _query:
            os.system('taskmgr')

        elif 'restart' in _query:
            os.system('shutdown -r')

        elif 'shutdown' in _query:
            os.system('shutdown -h')

        # basic information
        elif 'time' in _query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            speak('Current time is ' + time)
            """
            extra code: 
            strTime = datetime.datetime.now().strftime('%H:%M:%S')
            speak(f'The time is {strTime}')
            """

        elif "day" in _query:
            year = int(datetime.datetime.now().strftime('%Y'))
            month = int(datetime.datetime.now().strftime('%m'))
            day = int(datetime.datetime.now().strftime('%d'))
            week_day = calendar.weekday(year, month, day)
            day_name = calendar.day_name[week_day]
            # print(day_name)
            speak(f'today is {day_name}')

        elif 'date' in _query:
            dateToday = datetime.datetime.now().strftime('%Y-%m-%d')
            speak(f'the date is {dateToday}')

        elif 'weather' in _query:
            owm = pyowm.OWM('604c5862add216fc85112ca19d69ce7f')

            city = "Gaibandha, Gobindaganj"
            location = owm.weather_manager().weather_at_place(city)
            weather = location.weather
            temp = weather.temperature(unit='celsius')
            status = weather.detailed_status
            cleaned_temp_data = (int(temp['temp']))
            speak(f'The temperature today in {city} is {cleaned_temp_data} Degrees celsius')
            speak(f'The day today will have {status}')

        elif 'who is' in _query:
            person = _query.replace('who is', '')
            person_info = wikipedia.summary(person, 2)
            speak(person_info)

        elif 'what is' in _query:
            thing = _query.replace('what is', '')
            thing_details = wikipedia.summary(thing, 2)
            speak(thing_details)

        elif 'play' in _query:
            song = _query.replace('play', '')
            speak(f'playing {song}')
            pywhatkit.playonyt(song)

        elif 'search' in _query:
            topic = _query.replace('search', '')
            speak(f'Searching {topic}')
            pywhatkit.search(topic)

        elif 'news' in _query:
            url = 'https://en.prothomalo.com'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            headlines = soup.find_all(attrs={"class": "newsHeadline-m__title-link__1puEG"})
            for headline in headlines:
                print(headline.text)
                speak(headline.text)