import json


def get_voice():
    text_file = open(r"data\general.json", "r")
    json_string = text_file.read()
    text_file.close()

    voice = json.loads(json_string)
    return voice


def chnage_voice(voice):
    json_string = json.dumps(voice, indent=4)

    text_file = open(r"data\general.json", "w")
    text_file.write(json_string)
    text_file.close()


def add_command(type, command):
    commands = get_commands()
    commands[type].append(command)
    json_string = json.dumps(commands, indent=4)

    text_file = open(r"data\commands.json", "w")
    text_file.write(json_string)
    text_file.close()


def get_commands():
    text_file = open(r"data\commands.json", "r")
    json_string = text_file.read()
    text_file.close()

    commands = json.loads(json_string)
    return commands


def rem_command(type, id):
    text_file = open(r"data\commands.json", "r+")
    json_string = text_file.read()

    commands = json.loads(json_string)
    commands[type].pop(id)
    json_string = json.dumps(commands, indent=4)

    text_file.seek(0) 
    text_file.truncate(0)
    text_file.write(json_string)
    text_file.close()


def add_music(path):
    music = get_music()
    music.append(path)
    json_string = json.dumps(music, indent=4)

    text_file = open(r"data\music.json", "w")
    text_file.write(json_string)
    text_file.close()


def get_music():
    text_file = open(r"data\music.json", "r")
    json_string = text_file.read()
    text_file.close()

    music = json.loads(json_string)
    return music


def rem_music(id):
    text_file = open(r"data\music.json", "r+")
    json_string = text_file.read()

    music = json.loads(json_string)
    music.pop(id)
    json_string = json.dumps(music, indent=4)

    text_file.seek(0) 
    text_file.truncate(0)
    text_file.write(json_string)
    text_file.close()


def add_video(path):
    videos = get_videos()
    videos.append(path)
    json_string = json.dumps(videos, indent=4)

    text_file = open(r"data\videos.json", "w")
    text_file.write(json_string)
    text_file.close()


def get_videos():
    text_file = open(r"data\videos.json", "r")
    json_string = text_file.read()
    text_file.close()

    videos = json.loads(json_string)
    return videos


def rem_video(id):
    text_file = open(r"data\videos.json", "r+")
    json_string = text_file.read()

    videos = json.loads(json_string)
    videos.pop(id)
    json_string = json.dumps(videos, indent=4)

    text_file.seek(0) 
    text_file.truncate(0)
    text_file.write(json_string)
    text_file.close()


def add_program(path, name):
    programs = get_programs()
    programs.append({"name": name, "path": path})
    json_string = json.dumps(programs, indent=4)

    text_file = open(r"data\programs.json", "w")
    text_file.write(json_string)
    text_file.close()


def get_programs():
    text_file = open(r"data\programs.json", "r")
    json_string = text_file.read()
    text_file.close()

    programs = json.loads(json_string)
    return programs


def rem_program(id):
    text_file = open(r"data\programs.json", "r+")
    json_string = text_file.read()

    programs = json.loads(json_string)
    programs.pop(id)
    json_string = json.dumps(programs, indent=4)

    text_file.seek(0) 
    text_file.truncate(0)
    text_file.write(json_string)
    text_file.close()
