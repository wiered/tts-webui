import asyncio
from fastapi import FastAPI, Request, Form, status
from fastapi.responses import FileResponse
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from audio import TTSGen, AudioOut
from db import *
from utils import getDevices

app = FastAPI()
tts_gen = TTSGen("ru")
audio_out = AudioOut()
audio_out.initMixer()

templates = Jinja2Templates(directory="./src/webui/templates")
app.mount("/static", StaticFiles(directory="./src/webui/static"), name="static")
favicon_path = './src/webui/favicon.ico'

sounds = load_sounds_from_file()

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "sounds": sounds,
                                       "devices": getDevices(False),
                                       })

@app.post("/add")
async def add_sound(request: Request, text: str = Form(...), filename: str = Form(...)):
    url = app.url_path_for("root")

    if text == "":
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

    if filename == "":
        filename = tts_gen.generateFileFromText(text)

    sounds.append({"filename": filename, "text": text})

    save_sounds_to_file(sounds)


    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/play")
async def play_sound(request: Request, text: str = Form(...)):
    if text != "":
        sound = await asyncio.to_thread(tts_gen.generateFromText, text)
        await asyncio.to_thread(audio_out.playSound, sound)

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.post("/select")
async def select_device(request: Request, device: str = Form(...)):
    audio_out.stopMixer()
    audio_out.initMixer(device)

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/play/{sound_filename}")
async def play_file(request: Request, sound_filename: str):
    await asyncio.to_thread(audio_out.playSoundFromFile, sound_filename)

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/stop")
async def stop(request: Request):
    audio_out.stopMixer()
    audio_out.initMixer()

    url = app.url_path_for("root")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
