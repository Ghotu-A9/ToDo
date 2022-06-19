from gtts import gTTS
from io import BytesIO
import pyglet


class VoiceUtility:
    def __init__(self, app):
        self.App = app

    def directPlayFromGoogle(self, sentence):
        tts = gTTS(sentence, lang='en')
        myMP3 = BytesIO()
        tts.write_to_fp(myMP3)
        myMP3.seek(0)
        test = pyglet.media.load(None, file=myMP3, streaming=False)
        test.play()
