import requests
import nltk
import google
import little_dude

import voices as vc

def init(query):
    for word in ["who", "whom", "whose", "which", "what", "where", "why", "how", "when"]:
        query.replace(word, '')

    r = requests.get("https://api.duckduckgo.com",
        params = {
            "q": query,
            "format": "json"
        })

    data = r.json()

    source = data["AbstractSource"]
    answer = data["AbstractText"]
    link = data["AbstractURL"]
    tokens = nltk.sent_tokenize(answer)

    if source != "" and answer != "":
        little_dude.change_face("happy")
        sentence = "According to " + source + ". " + tokens[0] + " " + tokens[1]
        vc.send_to_window("Full info: " + link)
        vc.say(sentence)
    else:
        little_dude.change_face("questinable")
        vc.say("Couldn't find anything myself. But I'll open google for you.")

        google.init(query)
