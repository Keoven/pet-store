# syntax=docker/dockerfile:1
FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["uvicorn", "pet_store.main:app", "--host", "0.0.0.0"]
