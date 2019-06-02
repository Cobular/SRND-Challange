FROM python:3.7-alpine

RUN adduser -D srndchallenge

WORKDIR /home/srndchallenge

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY srndchallengepackage srndchalengepackage
COPY run.py config.py run.sh codeday.db3 ./
RUN chmod +x run.sh

RUN chown -R srndchallenge:srndchallenge ./
USER srndchallenge

ENTRYPOINT ["./run.sh"]
