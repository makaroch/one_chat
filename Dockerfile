FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD python main.py
