import os
import shutil
from pathlib import Path
from pydub import AudioSegment
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from fastapi import APIRouter, Response, status
from fastapi import UploadFile, File, Form, Depends
from fastapi.responses import FileResponse

from src.database.engine import get_db
from src.config import AUDIO_DIR
from src.database.models import User, Audio
from src.schemas import CreateUserResponse, CreateUserRequest, UploadAudioResponse

audio_convertor_router = APIRouter(prefix='', tags=['audio_convertor'])


async def validate_user(db: AsyncSession, user_id: str, access_token: str) -> User:
    user_query = select(User).where(User.id == user_id, User.access_token == access_token)
    result = await db.execute(user_query)
    user = result.scalar()
    return user


@audio_convertor_router.post("/users", summary="Создать пользователя.")
async def create_user(
        response: Response,
        create_user_data: CreateUserRequest,
        db: AsyncSession = Depends(get_db)
) -> CreateUserResponse | dict:
    try:
        user_with_username_query = select(User).where(User.username == create_user_data.username)
        result = await db.execute(user_with_username_query)
        user = result.scalar()
        if user:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "User with this username already exists."}
        token = str(uuid4())
        user = User(username=create_user_data.username, access_token=token)
        db.add(user)
        await db.commit()
        return CreateUserResponse(user_id=str(user.id), access_token=token)
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@audio_convertor_router.post("/audio", summary="Загрузить WAV-файл для конвертации в MP3.")
async def upload_audio(
        response: Response,
        user_id: str = Form(description="ID пользователя"),
        access_token: str = Form(description="Токен пользователя"),
        file: UploadFile = File(description="WAV-файл"),
        db: AsyncSession = Depends(get_db),
) -> UploadAudioResponse | dict:
    try:
        user = await validate_user(db, user_id, access_token)
        if not user:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "User with this user_id and access_token not found."}
        filename = file.filename or "audio.wav"
        ext = Path(filename).suffix.lower()
        if ext not in (".wav", ".wave") or file.content_type not in ("audio/wav", "audio/x-wav", "audio/wave"):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Only WAV format available."}

        audio_id = str(uuid4())
        temp_wav_path = f"{AUDIO_DIR}/{audio_id}.wav"
        mp3_path = f"{AUDIO_DIR}/{audio_id}.mp3"

        try:
            with open(temp_wav_path, "wb") as out:
                shutil.copyfileobj(file.file, out)
            sound = AudioSegment.from_wav(str(temp_wav_path))
            sound.export(str(mp3_path), format="mp3")
            audio = Audio(
                id=audio_id,
                user_id=user.id,
                filename=filename,
                mp3_path=str(mp3_path),
            )
            db.add(audio)
            await db.commit()

            download_url = f"/audio/{audio_id}"
            return UploadAudioResponse(audio_id=str(audio_id), download_url=download_url)
        finally:
            if os.path.exists(temp_wav_path):
                try:
                    os.remove(temp_wav_path)
                except Exception:
                    pass
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}


@audio_convertor_router.get("/audio/{audio_id}", summary="Скачать MP3-файл.")
async def get_audio(
        response: Response,
        audio_id: str,
        db: AsyncSession = Depends(get_db)
):
    try:
        audio_query = select(Audio).where(Audio.id == audio_id)
        result = await db.execute(audio_query)
        audio = result.scalar()
        if not audio:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Audio with this audio_id doesn`t exist."}

        file_path = Path(audio.mp3_path)
        if not file_path.exists():
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"detail": "Audio not found."}

        return FileResponse(
            path=str(file_path),
            media_type="audio/mpeg",
            filename=f"{audio_id}.mp3",
        )
    except Exception as e:
        print(e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"detail": "An unexpected error occurred. Contact your administrator."}
