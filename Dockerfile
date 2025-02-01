FROM python:slim-bookworm
COPY . /crawler 
WORKDIR /crawler
RUN pip install -r requirements.txt
RUN pip install -e .
CMD [ "python", "Main.py" ]