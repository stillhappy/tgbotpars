FROM python:3.12.1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]