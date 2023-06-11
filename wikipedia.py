import webbrowser
import little_dude

import voices as vc

def init():
    try:
        vc.say("What would you like to learn about?")

        desired = vc.get()

        webbrowser.open('https://wikipedia.org/w/index.php?search=' + desired)
        little_dude.change_face("happy")
    except:
        vc.say("Something went wrong. Check your internet connection.")
        little_dude.change_face("static")