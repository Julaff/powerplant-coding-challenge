FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install poetry

RUN poetry install

ENV PYTHONPATH="${PYTHONPATH}:/app/src/powerplant_coding_challenge"

#ENTRYPOINT ["poetry", "run", "python", "-m", "powerplant_coding_challenge.app"]
