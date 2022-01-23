from fastapi import FastAPI
from starlette.responses import StreamingResponse

from settings import token as main_token
from settings.custom_logger import Logger
from src.system_info import SystemMonitor

logger = Logger.make_logger()

app = FastAPI()
SystemMonitor().start()
app.logger = logger


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/show_ps_stat/{token}")
def image_endpoint(token: str):
    if token != main_token['token']:
        return {'error': True, 'reason': 'fuck off'}
    img = open('test.png', 'r+b')
    return StreamingResponse(img, media_type="image/png")


@app.get("/show_ps_stat_in_text/{token}")
async def pc_status_in_json(token: str):
    if token != main_token['token']:
        return {'error': True, 'reason': 'fuck off'}
    return SystemMonitor.data_pool[-1]
