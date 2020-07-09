FROM python:3

WORKDIR /usr/src/app

COPY ./requirments.txt ./
RUN pip install -r requirments.txt
COPY ./ ./
RUN chmod 600 id_rsa

ENTRYPOINT [ "python", "main.py" ]
