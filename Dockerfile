FROM python:slim-bookworm
COPY . /crawler 
RUN mkdir /logs
WORKDIR /crawler
RUN pip install -r requirements.txt
RUN pip install -e .
CMD [ "python", "Main.py" ]