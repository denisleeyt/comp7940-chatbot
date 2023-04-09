FROM python:3.9-slim-buster
WORKDIR /app
COPY requirements.txt /app/
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN apt-get update && apt-get install -y gcc && pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "parkinglot.py"]
