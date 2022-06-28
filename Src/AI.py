import pyttsx3

def speak(text):
    engine = pyttsx3.init()


    voices = engine.getProperty('voices')

    print(voices[29].name)

    engine.setProperty('voice',voices[11].id) #Eng

    engine.say(text)
    engine.runAndWait()


speak('Hello')
