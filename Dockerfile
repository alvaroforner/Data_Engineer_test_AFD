FROM ubuntu:latest

ENV TERM linux
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && apt-get install -y gnupg wget
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update -y && apt-get install -y google-chrome-stable python3-pip

COPY requirements.txt requirements.txt
RUN python3 -V
RUN pip install -r requirements.txt
