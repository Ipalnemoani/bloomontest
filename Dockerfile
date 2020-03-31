FROM python:3.7

LABEL maintainer="vlysenko"
LABEL Name=bloomon

WORKDIR /BloomonTest
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /BloomonTest
CMD ["python3", "main.py"]
