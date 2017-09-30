# Version: 0.0.1
# Origin docker image
FROM ubuntu
MAINTAINER Bogdan Lashkov <i@bogdan.co>
RUN ["apt-get", "update", "--fix-missing"]
RUN ["apt-get", "dist-upgrade", "-y"]
RUN ["apt-get", "install", "python3.5", "python3-pip", "-y"]
RUN alias python=python3.5 \
&& pip3 install --upgrade pip \
&& pip3 install --upgrade setuptools \
&& pip3 install --upgrade wheel \
&& pip3 install python-telegram-bot --upgrade

#Build this docker image
#docker build -t python3env .