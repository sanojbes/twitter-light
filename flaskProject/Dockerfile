FROM ubuntu:latest
LABEL authors="felixschussler"

ENTRYPOINT ["top", "-b"]

# Verwende ein Python-Image als Basis
FROM python:3.9

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die `requirements.txt`-Datei in den Container
COPY requirements.txt .

# Installiere die erforderlichen Python-Pakete
RUN pip install -r requirements.txt

# Kopiere den gesamten App-Ordner in den Container
COPY . .

# Exponiere den Port, den deine Flask-App verwenden wird
EXPOSE 5000

# Definiere den Befehl, der deine App startet
CMD ["python", "app.py"]
