FROM python:3.8-slim-buster

WORKDIR /error-correction-service
COPY . /error-correction-service

RUN pip3 install -r requirements.txt 

ENTRYPOINT [ "python" ]

CMD ["ec-app.py" ]