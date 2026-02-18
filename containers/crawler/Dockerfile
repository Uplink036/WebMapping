FROM python:3.12-slim

WORKDIR /app
COPY ./README.md .
COPY ./pyproject.toml . 
COPY ./src ./src

RUN pip install -e .[crawler]

CMD ["python", "./src/webmap/main.py"]
