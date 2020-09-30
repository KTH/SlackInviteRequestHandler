FROM python:3.7-alpine

WORKDIR repo

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
COPY run.py run.py

RUN apk add curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH = "${PATH}:/root/.poetry/bin"
ENV FLASK_APP=run.py

RUN poetry install

CMD ["poetry", "run", "flask", "run"]