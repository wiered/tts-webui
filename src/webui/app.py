from fastapi import FastAPI, Request, Form, status
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from audio import TTSGen, AudioOut
from utils import getDevices

app = FastAPI()
tts_gen = TTSGen("ru")
audio_out = AudioOut()
audio_out.initMixer()

templates = Jinja2Templates(directory="./src/webui/templates")
app.mount("/static", StaticFiles(directory="./src/webui/static"), name="static")

sounds = []

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "sounds": sounds,
                                       "devices": getDevices(False),
                                       })

@app.post("/add")
def add_sound(request: Request, text: str = Form(...)):
    sound = tts_gen.generateFileFromText(text)
    sounds.append({"filename": sound, "text": text})

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/select")
def select_device(request: Request, device: str = Form(...)):
    audio_out.stopMixer()
    audio_out.initMixer(device)

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/play/{sound_filename}")
def play(request: Request, sound_filename: str):
    audio_out.playSoundFromFile(sound_filename)

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
