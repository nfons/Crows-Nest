FROM jfloff/alpine-python:2.7-slim
MAINTAINER Nate Fonseka
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]