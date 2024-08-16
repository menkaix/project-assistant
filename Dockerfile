# Use the official Python 3.8 slim image as the base image
FROM python:3.8-slim

# Set the working directory within the container
WORKDIR /api-flask

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV FLASK_PORT=5000

CMD ["python","main.py"]