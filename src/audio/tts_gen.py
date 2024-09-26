import io

from gtts import gTTS

from utils import utils


class TTSGen():
    def __init__(self, language: str = "en"):
        self.language = language

    def generateFromText(self, text) -> io.BytesIO:
        sound_fp = io.BytesIO()
        gTTSobj = gTTS(text=text, lang=self.language, slow=False)
        gTTSobj.write_to_fp(sound_fp)
        sound_fp.seek(0)

        return sound_fp

    def generateFileFromText(self, text):
        salt = utils.generateSalt()
        filename = f"{salt}tts.mp3"
        gTTSobj = gTTS(text=text, lang=self.language, slow=False)
        gTTSobj.save("sounds/" + filename)

        return filename
