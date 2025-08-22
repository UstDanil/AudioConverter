<h1 align="center">Конвертер из WAV аудиозаписей в MP3</h1>


##  Описание ##

Создаётся пользователь, он имеет возможность загрузить WAV файл для конвертации его в MP3. 



##  Используемые технологии ##

- Python
- FastAPI
- SQLAlchemy
- asyncpg
- Poetry
- Docker
- uvicorn
- Pylint
- pydub
- ffmpeg
- python-multipart


##  Инструкция по запуску ##

1. На основе файла ```.env.example``` составить файл переменных окружений ```.env```

2. Через терминал, в папке с проектом ```docker compose up - d```



##  Результат ##

1. Новый пользователь создается методом POST. Путь "/users". 
```
Request: body
{
  "username": "Oleg"
} 
Response: 
{
    "user_id": "b5452bc8-69fe-443b-be15-e1e84f761ec6",
    "access_token": "9619b6ee-f824-41df-b7c2-dadef0b204cc"
}
```

2. Загрузка пользователем аудиозаписи формата WAV методом POST. Путь "/audio". 
```
Request: multipart/form-data
- user_id: uuid
- access_token: uuid
- file: file
Response:
{
  "audio_id": "b8321b5d-0c50-4ee4-8db3-29a5bd8f7d6b",
  "download_url": "/audio/b8321b5d-0c50-4ee4-8db3-29a5bd8f7d6b"
}
```

3. Получение аудиозаписи методом GET. Путь "audio/{audio_id}".
```
Request: path 
- audio_id: uuid 
Response: file
```