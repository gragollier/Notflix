FROM python

WORKDIR /usr/src/app

RUN apt-get update;apt-get install ffmpeg gpac -y
COPY ./requirments.txt ./
RUN pip install -r requirments.txt

COPY . .

# CMD ["python", "-u main.py"]
ENTRYPOINT [ "python", "main.py" ]
