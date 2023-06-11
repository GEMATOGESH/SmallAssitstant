import random

def init(ww):
	global window

	window = ww


def change_body(type=""):
	source = "textures/body/body" + str(type) + ".png"
	window.change_body(source)


def change_face(type="static"):
	id = random.randint(0, 2)
	if type == "static":
		faces = ["anime.png", "aufs.png", "what.png"]
		source = "textures/face/static/" + faces[id]
	elif type == "happy":
		faces = ["cool.png", "exited.png", "happy af.png"]
		source = "textures/face/happy/" + faces[id]
	elif type == "questinable":
		faces = ["empty.png", "questening.png", "sad.png"]
		source = "textures/face/questinable/" + faces[id]
	elif type == "none":
		source = "textures/face/none.png"

	window.change_face(source)
