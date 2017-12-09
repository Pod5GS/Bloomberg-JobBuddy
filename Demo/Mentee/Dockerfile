FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /Demo
WORKDIR /Demo
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "run.py"]