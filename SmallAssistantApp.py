import kivy

import music_command as music
import videos_command as videos
import programs_command as programs
import google
import wikipedia
import dao
import calculate
import joke
import weather
import question
import little_dude

import voices as vc

from settinglayout import SettingsLayout
from confirmationpopuplayout import ConfirmationPopupLayout
from printpopuplayout import PrintPopupLayout
from errorpopuplayout import ErrorPopupLayout
from programpopuplayout import ProgramPopupLayout

from threading import Thread
from functools import partial

from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.config import Config
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


Config.set('graphics', 'resizable', False)


def get_standard_commands_array():
    return ["music", "videos", "program", "google", "wikipedia", "calculate", "joke", "weather", "exit"]


def get_standard_folders_array():
    return ["music_folder", "videos_folder"]


def get_standard_commands_string():
    return "Standard commands: music, videos, program, google, wikipedia, calculate, joke, weather, exit"


class MainLayout(Screen):
    def change_mode(self, mode):
        global bot_mode
        global user_mode

        if mode == "bot":
            if bot_mode == "voice":
                self.ids.bot_mode_img.source = "textures/icon_text.png"
                self.ids.bot_mode_label.text = "Text"
                bot_mode = "text"
            elif bot_mode == "text":
                self.ids.bot_mode_img.source = "textures/icon_voice.png"
                self.ids.bot_mode_label.text = "Voice"
                bot_mode = "voice"
        elif mode == "user":
            if user_mode == "voice":
                self.ids.user_mode_img.source = "textures/icon_text.png"
                self.ids.user_mode_label.text = "Text"
                user_mode = "text"
            elif user_mode == "text":
                self.ids.user_mode_img.source = "textures/icon_voice.png"
                self.ids.user_mode_label.text = "Voice"
                user_mode = "voice"


    def open_settings(self):
        global sm
        sm.current('settings')


    @mainthread
    def change_body(self, source):
        self.ids.little_dude_body.source = source


    @mainthread
    def change_face(self, source):
        self.ids.little_dude_face.source = source


    @mainthread
    def log(self, text):
        text_input = self.ids.log_text_input
        if text_input.text != "":
            text_input.text += "\n"
        text_input.text += text


    @mainthread
    def reenable_buttons(self):
        self.ids.user_mode_box.opacity = 1
        self.ids.user_mode_box.disabled = False
        self.ids.bot_mode_box.opacity = 1
        self.ids.bot_mode_box.disabled = False
        self.ids.start_btn.opacity = 1
        self.ids.start_btn.disabled = False
        self.hide_main_input()

        event_thread.join()


    @mainthread
    def clear_main_textinput(self):
        self.ids.main_text_input.text = ""


    @mainthread
    def show_main_input(self):
        self.ids.main_text_input.opacity = 1
        self.ids.main_text_input.disabled = False


    @mainthread
    def hide_main_input(self):
        self.ids.main_text_input.opacity = 0
        self.ids.main_text_input.disabled = True


    def event_loop(self):
        commands = dao.get_commands()
        vc.set_modes(bot_mode, user_mode)
        vc.say("Enter a command.")

        while True:
            self.log(get_standard_commands_string())

            try:
                command = vc.get()
            except:
                self.reenable_buttons()
                return

            if command == "music" or command in commands["music"]:
                little_dude.change_face("none")
                little_dude.change_body("_headphones")
                music.init()

            elif command == "videos" or command in commands["videos"]:
                little_dude.change_face("none")
                little_dude.change_body("_popcorn")
                videos.init()

            elif command == "program" or command in commands["program"]:
                little_dude.change_face("none")
                little_dude.change_body("_explorer")
                programs.init()

            elif command == "google" or command in commands["google"]:
                little_dude.change_face("none")
                little_dude.change_body("_google")
                google.init()

            elif command == "wikipedia" or command in commands["wikipedia"]:
                little_dude.change_face("none")
                little_dude.change_body("_wikipedia")
                wikipedia.init()

            elif command == "calculate" or command in commands["calculate"]:
                little_dude.change_face("none")
                little_dude.change_body("_calculator")
                calculate.init()

            elif command == "joke" or command in commands["joke"]:
                little_dude.change_face("none")
                little_dude.change_body("_joke")
                joke.init()

            elif command == "weather" or command in commands["weather"]:
                little_dude.change_face("none")
                little_dude.change_body("_weather")
                weather.init()

            elif command is not None and any(word in command for word in ["who", "whom", "whose", "which", "what", "where", "why", "how", "when"]):
                question.init(command)

            elif command == "exit" or command in commands["exit"]:
                vc.say("Goodbye.")
                self.reenable_buttons()
                break

            else:
                vc.say("Wrong command.")

            little_dude.change_body()
            vc.say("Anything else?")


    def start(self):
        global event_thread
        global user_mode

        self.ids.user_mode_box.opacity = 0
        self.ids.user_mode_box.disabled = True
        self.ids.bot_mode_box.opacity = 0
        self.ids.bot_mode_box.disabled = True
        self.ids.start_btn.opacity = 0
        self.ids.start_btn.disabled = True

        if user_mode == "text":
            self.show_main_input()

        self.log("Loading...")

        event_thread = Thread(target=self.event_loop, daemon=True)
        event_thread.start()


class SmallAssistantApp(App):
    def change_voice(self, id, instance):
        vc.change_voice(id)
        dao.chnage_voice(id)


    def add_voices_to_root(self, stack, voices):
        id = 0

        for voice in voices:
            btn = Button(text=str(voice), background_normal='textures/unpressed_button.png', background_down='textures/pressed_button.png')
            btn.size_hint = (None, None)
            btn.height = 80
            btn.width = 144
            btn.text_size = (btn.width, None)
            btn.halign = 'center'
            btn.padding = (10, 10)
            buttoncallback = None
            buttoncallback = partial(self.change_voice, id)
            btn.bind(on_press=buttoncallback)
            id += 1

            stack.add_widget(btn)

            if len(stack.children) % 5 == 0:
                stack.height += 90


    def add_to_root(self, root, values, value_type):
        names = []
        if value_type == "programs":
            for value in values:
                names += [value["name"]]
            values = names

        for value in values:
            btn = Button(text=str(value), background_normal='textures/unpressed_button.png', background_down='textures/pressed_button.png')
            btn.size_hint = (None, None)
            btn.height = 80
            btn.width = 144
            btn.text_size = (btn.width, None)
            btn.halign = 'center'
            btn.padding = (10, 10)
            buttoncallback = None
            buttoncallback = partial(self.remove_value, value_type, root)
            btn.bind(on_press=buttoncallback)

            root.add_widget(btn)

            if len(root.children) % 5 == 0:
                root.height += 90
        
        btn = Button(text=str("+"), background_normal='textures/unpressed_button.png', background_down='textures/pressed_button.png')
        btn.size_hint = (None, None)
        btn.height = 80
        btn.width = 144
        btn.text_size = (btn.width, None)
        btn.halign = 'center'
        btn.padding = (10, 10)
        buttoncallback = partial(self.add_value, value_type, root)
        btn.bind(on_press=buttoncallback)

        root.add_widget(btn)

    
    def btn_yes_confirmation_click(self, value_type, original_btn, popup, root, instance):
        values = None
        if value_type in get_standard_commands_array():
            values = dao.get_commands()[value_type]
        elif value_type in get_standard_folders_array():
            if value_type == get_standard_folders_array()[0]:
                values = dao.get_music()
            elif value_type == get_standard_folders_array()[1]:
                values = dao.get_videos()
        elif value_type == "programs":
            values = dao.get_programs()
        
        for i in range(0, len(values)):
            if value_type != "programs":
                if values[i] == original_btn.text:
                    if value_type in get_standard_commands_array():
                        dao.rem_command(value_type, i)
                    elif value_type in get_standard_folders_array():
                        if value_type == get_standard_folders_array()[0]:
                            dao.rem_music(i)
                        elif value_type == get_standard_folders_array()[1]:
                            dao.rem_video(i)
                    break
            else:
                if values[i]["name"] == original_btn.text:
                    dao.rem_program(i)
                    break

        root.remove_widget(original_btn)
        if len(root.children) % 5 == 0:
                root.height -= 90
        popup.dismiss()


    def btn_yes_print_click(self, value_type, plus_btn, popup, text_input, root, instance, path=None):
        if (len(text_input.text) <= 2) or (path is not None and len(path.text) <= 2):
            error_popup = ErrorPopupLayout()
            popup = Popup(title='Error', size=(400,200), size_hint=(None, None), content=error_popup, auto_dismiss=False)
            error_popup.ids.error_label.text = "String must contain at least 3 characters."
            popup.open()
            error_popup.ids.error_btn.bind(on_press=popup.dismiss)
            return
        
        error_text = None
        if value_type in get_standard_commands_array():
            commands = dao.get_commands()
            for command_type_values in commands.values():
                for command in command_type_values:
                    if command.replace(" ", "") == text_input.text.replace(" ", "").lower():
                        error_text = "Command already exists."
            commands = get_standard_commands_array()
            for command in commands:
                    if command.replace(" ", "") == text_input.text.replace(" ", "").lower():
                        error_text = "Command already exists."
            
                        
        elif value_type in get_standard_folders_array():
            folders = None
            if value_type == get_standard_folders_array()[0]:
                folders = dao.get_music()
            elif value_type == get_standard_folders_array()[1]:
                folders = dao.get_videos()

            for folder in folders:
                if folder.replace(" ", "") == text_input.text.replace(" ", "").lower():
                    error_text = "Folder already exists."

        elif value_type == "programs":
            programs = dao.get_programs()
            for program in programs:
                if (program["name"].replace(" ", "") == text_input.text.replace(" ", "").lower()) or (program["path"].replace(" ", "") == path.text.replace(" ", "")):
                    error_text = "Program or path already exists."
                
        if error_text is not None:
            error_popup = ErrorPopupLayout()
            popup = Popup(title='Error', size=(400,200), size_hint=(None, None), content=error_popup, auto_dismiss=False)
            error_popup.ids.error_label.text = error_text
            popup.open()
            error_popup.ids.error_btn.bind(on_press=popup.dismiss)
            return
        
        if value_type in get_standard_commands_array():
            dao.add_command(value_type, text_input.text.lower())
        elif value_type in get_standard_folders_array():
            if value_type == get_standard_folders_array()[0]:
                dao.add_music(text_input.text.lower())
            elif value_type == get_standard_folders_array()[1]:
                dao.add_video(text_input.text.lower())
        elif value_type == "programs":
            dao.add_program(path.text.lower(), text_input.text.lower())

        root.remove_widget(plus_btn)

        btn = Button(text=str(text_input.text.lower()), background_normal='textures/unpressed_button.png', background_down='textures/pressed_button.png')
        btn.size_hint = (None, None)
        btn.height = 80
        btn.width = 144
        btn.text_size = (btn.width, None)
        btn.halign = 'center'
        btn.padding = (10, 10)
        buttoncallback = partial(self.remove_value, value_type, root)
        btn.bind(on_press=buttoncallback)
        root.add_widget(btn)

        if len(root.children) % 5 == 0:
                root.height += 90

        btn = Button(text=str("+"), background_normal='textures/unpressed_button.png', background_down='textures/pressed_button.png')
        btn.size_hint = (None, None)
        btn.height = 80
        btn.width = 144
        btn.text_size = (btn.width, None)
        btn.halign = 'center'
        btn.padding = (10, 10)
        buttoncallback = partial(self.add_value, value_type, root)
        btn.bind(on_press=buttoncallback)
        root.add_widget(btn)

        popup.dismiss()


    def remove_value(self, value_type, root, instance):
        conf_popup = ConfirmationPopupLayout()
        
        label = conf_popup.ids.confirmation_popup_label
        title = None
        if value_type in get_standard_commands_array():
            label.text = "Are you sure you want to remove command '" + instance.text + "'?"
            title = 'Remove command'
        elif value_type in get_standard_folders_array():
            label.text = "Are you sure you want to remove '" + instance.text + "' folder?"
            title = 'Remove folder'
        elif value_type == "programs":
            label.text = "Are you sure you want to remove " + instance.text + "?"
            title = 'Remove program'
        
        popup = Popup(title=title, size=(400,200), size_hint=(None, None), content=conf_popup, auto_dismiss=False)
        popup.open()

        btn_no = conf_popup.ids.confirmation_popup_btn_no
        btn_no.bind(on_press=popup.dismiss)

        btn_yes = conf_popup.ids.confirmation_popup_btn_yes
        buttoncallback = partial(self.btn_yes_confirmation_click, value_type, instance, popup, root)
        btn_yes.bind(on_press=buttoncallback)


    def add_value(self, value_type, root, instance):
        popup_layout = None
        title = None
        if value_type != "programs":
            popup_layout = PrintPopupLayout()
            label = popup_layout.ids.print_popup_label
            if value_type in get_standard_commands_array():
                label.text = "Enter a command for '" + value_type + "' category:"
                title = 'Add command'
            elif value_type in get_standard_folders_array():
                label.text = "Enter a new folder path:"
                title = 'Add folder'
        else:
            popup_layout = ProgramPopupLayout()
            title = 'Add program'

        popup = Popup(title=title, size=(400,200), size_hint=(None, None), content=popup_layout, auto_dismiss=False)
        popup.open()

        btn_no = popup_layout.ids.print_popup_btn_no
        btn_no.bind(on_press=popup.dismiss)

        btn_yes = popup_layout.ids.print_popup_btn_yes
        buttoncallback = None
        if value_type != "programs":
            buttoncallback = partial(self.btn_yes_print_click, value_type, instance, popup, popup_layout.ids.popup_text_input, root)
        else:
            buttoncallback = partial(self.btn_yes_print_click, value_type, instance, popup, popup_layout.ids.popup_program_name_input, root, path=popup_layout.ids.popup_program_path_input)
        btn_yes.bind(on_press=buttoncallback)


    def build(self):
        global bot_mode
        global user_mode

        bot_mode = "voice"
        user_mode = "voice"

        self.icon = 'textures\\body\\body.png'

        sm = ScreenManager(transition=FadeTransition())

        mainScreen = MainLayout(name='main')

        little_dude.init(mainScreen)
        little_dude.change_body()
        little_dude.change_face()

        vc.init(mainScreen, dao.get_voice())
        
        settingsScreen = SettingsLayout(name='settings')

        self.add_voices_to_root(settingsScreen.ids.stack_voice, vc.get_voices())

        commands = dao.get_commands()
        self.add_to_root(settingsScreen.ids.stack_music, commands['music'], 'music')
        self.add_to_root(settingsScreen.ids.stack_videos, commands['videos'], 'videos')
        self.add_to_root(settingsScreen.ids.stack_program, commands['program'], 'program')
        self.add_to_root(settingsScreen.ids.stack_google, commands['google'], 'google')
        self.add_to_root(settingsScreen.ids.stack_wikipedia, commands['wikipedia'], 'wikipedia')
        self.add_to_root(settingsScreen.ids.stack_exit, commands['exit'], 'exit')
        self.add_to_root(settingsScreen.ids.stack_calculate, commands['calculate'], 'calculate')
        self.add_to_root(settingsScreen.ids.stack_joke, commands['joke'], 'joke')
        self.add_to_root(settingsScreen.ids.stack_weather, commands['weather'], 'weather')

        music_folders = dao.get_music()
        self.add_to_root(settingsScreen.ids.stack_music_folders, music_folders, 'music_folder')
        videos_folders = dao.get_videos()
        self.add_to_root(settingsScreen.ids.stack_videos_folders, videos_folders, 'videos_folder')

        programs = dao.get_programs()
        self.add_to_root(settingsScreen.ids.stack_programs, programs, 'programs')

        sm.add_widget(mainScreen)
        sm.add_widget(settingsScreen)

        return sm


if __name__ == "__main__":
    SmallAssistantApp().run()
