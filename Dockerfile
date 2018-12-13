FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
RUN ln -s /usr/bin/python3 /usr/local/bin/python

