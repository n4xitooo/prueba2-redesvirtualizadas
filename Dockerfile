FROM python:3.11-slim

ENV PIP_PROGRESS_BAR=off

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --progress-bar off -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
