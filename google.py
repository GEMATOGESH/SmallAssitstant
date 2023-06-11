import webbrowser
import little_dude

import voices as vc

def init(query = None):
    try:
        if query == None:
            vc.say("What would you like to search for?")

            query = vc.get()

            if query == "exit":
                little_dude.change_face("static")
                return

        webbrowser.open('https://www.google.by/search?q=' + query)
        little_dude.change_face("happy")
    except:
        vc.say("Something went wrong. Check your internet connection.")
        little_dude.change_face("static")
        return