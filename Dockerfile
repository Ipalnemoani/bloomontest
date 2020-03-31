FROM python:3.7

LABEL maintainer="vlysenko"
LABEL Name=bloomon

WORKDIR /
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . /
CMD ["python3", "main.py"]
