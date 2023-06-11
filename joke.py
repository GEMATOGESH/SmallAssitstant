import requests
import little_dude

import voices as vc

def init():
    try:
        response = requests.get('https://icanhazdadjoke.com', headers={"Accept":"application/json"})
        joke = response.json()['joke']
        
        vc.say(joke) 
        little_dude.change_face("happy")
    except:
        vc.say("Something went wrong. Check your internet connection.")
        little_dude.change_face("static")
        return