FROM python:slim-bookworm

COPY . /crawler 
RUN mkdir /logs
WORKDIR /crawler
RUN pip install -r requirements.txt
RUN pip install -e .

ENV SCRUB_DB=0
CMD [ "python", "Main.py" ]