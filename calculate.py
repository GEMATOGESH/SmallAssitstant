import little_dude

import voices as vc

def init():
    while True:
        vc.say("Enter expression.")

        vc.send_to_window("Available operations: +, -, *, / and brackets.")

        expression = vc.get()

        if expression == "exit":
            little_dude.change_face("static")
            return

        elif any(char not in ["+", "-", "*", "/", " ", "(", ")", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] for char in expression):
            little_dude.change_body()
            little_dude.change_face("questinable")
            vc.say("Unsupported operation found in expression. Try again.")
            little_dude.change_body("_calculator")
            little_dude.change_face("none")
            continue

        else:
            result = eval(expression)
            vc.say("Result is " + str(round(result, 2)))
            little_dude.change_face("happy")
            return