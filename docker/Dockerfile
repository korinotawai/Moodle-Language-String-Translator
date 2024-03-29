# app/Dockerfile

FROM python:3.11-slim

WORKDIR /Moodle-Language-String-Translator

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/korinotawai/Moodle-Language-String-Translator.git .

RUN pip3 install -r requirements.txt

RUN python -m nltk.downloader punkt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "translate.py", "--server.port=8501", "--server.address=0.0.0.0"]
