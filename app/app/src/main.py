from fastapi import FastAPI

from src.router import audio_convertor_router
from src.database.engine import create_tables_async

app = FastAPI()

app.include_router(audio_convertor_router)


@app.on_event("startup")
async def startup_event():
    await create_tables_async()


@app.get("/")
def root():
    return {
        "endpoints": {
            "POST /users": "Создать пользователя по username",
            "POST /audio": "Загрузить WAV, указав user_id и access_token",
            "GET /audio/{audio_id}": "Скачать MP3 по UUID",
        }
    }
