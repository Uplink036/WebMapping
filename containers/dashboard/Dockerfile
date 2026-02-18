FROM python:3.12-slim

WORKDIR /app
COPY ./README.md .
COPY ./pyproject.toml . 
COPY ./src ./src

RUN pip install -e .[dashboard]
EXPOSE 8000

CMD ["uvicorn", "dashboard.api:app", "--host", "0.0.0.0", "--port", "8000"]
