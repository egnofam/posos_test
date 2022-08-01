FROM python:3.9.13-slim-buster

WORKDIR /app/posology

# copy source code
COPY ./src/api .

# install python packages
RUN pip3 install -r requirements.txt

EXPOSE 4002

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4002"]
