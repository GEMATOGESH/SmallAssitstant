import json
import requests
import little_dude
import os

import voices as vc

from dotenv import load_dotenv

def init():
    try:
        location = requests.get('http://ipinfo.io/json').json()['city']
        load_dotenv()
        api_key = os.getenv('weather')

        result = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + api_key + "&units=metric").json()
        feels_like = round(result["main"]["feels_like"])
        desc = result["weather"][0]["description"]
        temp = result["main"]["temp"]

        sentence = "The weather in " + str(location) + ": " + str(int(temp)) + "°C, feels like " + str(feels_like) + "°C with " + str(desc) + "."
        vc.say(sentence) 
        little_dude.change_face("happy")
    except:
        vc.say("Something went wrong. Check your internet connection.")
        little_dude.change_face("static")