from pydantic import BaseModel, field_validator


class CreateUserRequest(BaseModel):
    username: str

    @field_validator('username', mode='after')
    def validate_username(cls, value) -> str:
        value = value.strip()
        if not value:
            raise ValueError("username не может быть пустым.")
        return value


class CreateUserResponse(BaseModel):
    user_id: str
    access_token: str


class UploadAudioResponse(BaseModel):
    audio_id: str
    download_url: str
