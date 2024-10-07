FROM python:3.12.6

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ /app/src/
COPY assets/ /app/assets/

CMD ["python", "src/main.py"]
