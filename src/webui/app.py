from fastapi import FastAPI, Request

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="./src/webui/templates")

app = FastAPI()

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
