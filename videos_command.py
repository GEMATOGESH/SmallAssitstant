import glob
import os
import dao
import little_dude

import numpy as np 
import voices as vc

from random import randint

def init():
    paths = dao.get_videos()

    name = os.getlogin()
    paths.append("C:\\Users\\" + name + "\\Videos")

    exts = ["mp4", "mov", "wmv", "flv", "avi", "avchd", "webm", "mkv"]

    files = []
    for path in paths:
        for ext in exts:
            files_glob = glob.glob(path + "/**/*." + ext, recursive=True)
            files = np.append(files, files_glob)

    if len(files) == 0:
        vc.say("I couldn't find anything. Check your settings.")
        little_dude.change_face("static")
        return

    vc.say("Here's what I found in your videos folder. Do you want anything specific?")

    for file in files:
        vc.send_to_window(os.path.basename(file))

    main_choice(files)


def main_choice(files):
    while True:
        answer = vc.get()

        if answer == "yes":
            something_special(files)
            return

        elif answer == "no":
            vc.say("Okay, I'll play a random video.")
            number = randint(0, len(files) - 1)
            os.startfile('"' + files[number] + '"')
            little_dude.change_face("happy")
            return

        elif answer == "exit":
            vc.say("Okay, returning.")
            little_dude.change_face("static")
            return

        else:
            little_dude.change_body()
            little_dude.change_face("questinable")
            vc.say("I didn't get that, try again.")
            little_dude.change_body("_popcorn")
            little_dude.change_face("none")
            continue


def something_special(files):
    while True:
        vc.say("Which one to play?")
        video_track = vc.get()

        if video_track == None:
            little_dude.change_body()
            little_dude.change_face("questinable")
            vc.say("I couldn't find the file you want, try again.")
            little_dude.change_body("_popcorn")
            little_dude.change_face("none")
            continue

        similar = []
        for file in files:
            if video_track.lower() in file.lower():
                similar.append(file)

        if len(similar) == 1:
            vc.say("Starting")
            os.startfile('"' + similar[0] + '"')
            little_dude.change_face("happy")
            break

        elif len(similar) > 1:
            vc.say("Here's a files that I think you meant, which one to play?")
            for i in range(0, len(similar)):
                vc.send_to_window(str(i + 1) + ". " + os.path.basename(similar[i]))

            while True:
                number = vc.get()

                if not number.isnumeric() and number != "exit":
                    little_dude.change_body()
                    little_dude.change_face("questinable")
                    vc.say("There's no video with this number. Try again.")
                    little_dude.change_body("_popcorn")
                    little_dude.change_face("none")
                    continue

                elif number == "exit":
                    break

                if 0 < int(number) <= len(similar):
                    vc.say("Starting")
                    os.startfile('"' + similar[int(number) - 1] + '"')
                    little_dude.change_face("happy")
                    break

                else:
                    little_dude.change_body()
                    little_dude.change_face("questinable")
                    vc.say("There's no video with that number. Try again.")
                    little_dude.change_body("_popcorn")
                    little_dude.change_face("none")
            break

        elif len(similar) == 0:
            little_dude.change_body()
            little_dude.change_face("questinable")
            vc.say("I couldn't find the file you want, try again.")
            little_dude.change_body("_popcorn")
            little_dude.change_face("none")

        elif similar == "exit":
            break
        