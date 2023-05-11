FROM python:3.9-slim

WORKDIR /usr/src

COPY ./app /usr/src/app

RUN apt-get update && apt-get install -y netcat

RUN chmod u+x ./app/entrypoint.sh

RUN pip install -r ./app/requirements.txt

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
