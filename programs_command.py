import os
import dao
import little_dude

import voices as vc

def init():
    programs = dao.get_programs()

    if len(programs) == 0:
        vc.say("I couldn't find anything. Check your settings.")
        little_dude.change_face("static")
        return

    vc.send_to_window("Available programs: ")
    for program in programs:
        vc.send_to_window(program["name"])

    while True:
        vc.say("Which program to open?")

        desired = vc.get()

        if desired == "exit":
            little_dude.change_face("static")
            break

        similar = []
        for program in programs:
            if desired in program["name"]:
                similar.append(program)

        if len(similar) == 1:
            vc.say("Opening")
            os.startfile('"' + similar[0]["path"] + '"')
            little_dude.change_face("happy")
            break

        elif len(similar) > 1:
            vc.say("Here are the programs that I think you meant, which one to open?")
            for i in range(0, len(similar)):
                vc.send_to_window(str(i + 1) + ". " + similar[i]["name"])

            while True:
                number = vc.get()

                if not number.isnumeric() and number != "exit":
                    little_dude.change_body()
                    little_dude.change_face("questinable")
                    vc.say("There's no program with this number. Try again.")
                    little_dude.change_body("_explorer")
                    little_dude.change_face("none")
                    continue

                elif number == "exit":
                    break

                if 0 < int(number) <= len(similar):
                    vc.say("Opening")
                    os.startfile('"' + similar[int(number) - 1]["path"] + '"')
                    little_dude.change_face("happy")
                    break

                else:
                    little_dude.change_body()
                    little_dude.change_face("questinable")
                    vc.say("There's no program with such number. Try again.")
                    little_dude.change_body("_explorer")
                    little_dude.change_face("none")
            break

        elif len(similar) == 0:
            little_dude.change_body()
            little_dude.change_face("questinable")
            vc.say("I couldn't find a program you want, try again.")
            little_dude.change_body("_explorer")
            little_dude.change_face("none")