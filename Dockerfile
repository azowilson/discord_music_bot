FROM ubuntu

WORKDIR /

ENV WEB_HOOK_KEY=OTM5MDYzNzU5NDQyNDM2MTM2.GWxpa4.NKrEqWWGY2Yruj4AcW4Ka50O0djZUxWA6eolys

RUN apt-get update && apt-get install -y ffmpeg

RUN apt-get install python3

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "main.py"]