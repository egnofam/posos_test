# base image
FROM python:3.9.13-slim-buster

ARG data_passwd

WORKDIR /app/posology

# copy source code
COPY ./src/train .

# install python packages
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
