FROM python:3.6.2
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt