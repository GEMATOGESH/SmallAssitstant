import pyttsx3
import threading

import speech_recognition as sr

def init(ww, vc):
    global engine
    global window

    window = ww

    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[vc].id)

    global recognizer
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

    engine.say("I'm ready.")
    engine.runAndWait()


def get_voices():
    voices = engine.getProperty('voices')
    res = []
    for voice in voices:
        res += [voice.name]

    return res


def change_voice(id):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[id].id)
    engine.say('Changed.')
    engine.runAndWait()


def set_modes(om, im):
    global input_mode
    global output_mode

    input_mode = im
    output_mode = om


def get():
    global recognizer
    global input_mode

    if input_mode == "voice":
        while True:
            send_to_window("I'm listening...")
            try:
                with sr.Microphone() as source:
                    audio = recognizer.listen(source)
                    send_to_window("Heard.")
                    said = recognizer.recognize_google(audio, language= 'en-US')
                    said = said.lower()
                    send_to_window("You said: " + said)
                    return said

            except sr.RequestError as e:
                sentence = "Could not request results. Check internet connection."
                say(sentence)
                raise Exception()

            except Exception:
                sentence = "Sorry, I didn't get that. Try again."
                say(sentence)

    elif input_mode == "text":
        send_to_window("Type your answer.")
        return get_with_text()       


def get_with_text(reason=None):
    if reason is not None:
        window.show_main_input()

    text_input = window.ids.main_text_input
    event = threading.Event()

    def result(self):
        text_input.unbind(on_text_validate=result)
        event.set()

    text_input.bind(on_text_validate=result) 
    event.wait()
    result = text_input.text
    send_to_window("You said: " + result)
    window.clear_main_textinput()

    if reason is not None:
        window.hide_main_input()
    return result 


def say(sentence):
    if output_mode != "text":
        engine.say(sentence)
        engine.runAndWait()

    window.log(sentence)


def send_to_window(sentence):
    window.log(sentence)