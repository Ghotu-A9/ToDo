import pyttsx3

engine = pyttsx3.init()

name = "Smora"


voices = engine.getProperty('voices')
engine.setProperty('voice', voices[3].id)

engine.say(name)

engine.runAndWait()
engine.stop()
