FROM python:3.12-alpine

RUN pip install poetry

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "linkedin_password_maximum_length/main.py"]
