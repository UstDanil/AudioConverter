FROM python:3.10

ENV PYTHONUNBUFFERED=1
RUN pip install "poetry==1.8.1"

RUN mkdir /application
WORKDIR /application

RUN apt-get update && apt-get install -y ffmpeg
COPY app/app/pyproject.toml /application

RUN poetry config virtualenvs.create false  \
    && poetry install --no-interaction --no-ansi

COPY ./app/app /application

ENV PYTHONPATH "/application"

RUN chmod +x /application/script.sh
CMD [ "sh", "-c", "/application/script.sh" ]