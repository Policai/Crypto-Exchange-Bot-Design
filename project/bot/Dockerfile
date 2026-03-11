FROM python:3.11-slim
WORKDIR /app
COPY bot/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app
WORKDIR /app/bot
CMD ["python", "bot.py"]
