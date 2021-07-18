FROM python:3.7 as base 

# Upgrade installed packages
RUN apt update && apt upgrade -y && apt clean

RUN apt-get update
RUN apt-get -y install ssh
RUN apt-get -y install python3-pip
RUN apt-get -y install htop
RUN apt-get -y install libpq-dev

RUN apt-get update 
RUN apt-get -y install cmake libopenmpi-dev python3-dev zlib1g-dev libgl1-mesa-dev

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools

ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8
ENV export LANG=C.UTF-8

# Nethack
# Python and most build deps
RUN apt-get update 
RUN apt-get install -y build-essential autoconf libtool pkg-config \
    python3-dev python3-pip python3-numpy git flex bison libbz2-dev

# recent cmake version
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
# RUN apt-get install gpg-agent -y
# RUN apt-get -y install python3-apt
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add -
RUN apt-get -y install software-properties-common
RUN apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main'
RUN apt-get update && apt-get --allow-unauthenticated install -y \
    cmake \
    kitware-archive-keyring


RUN useradd -ms /bin/bash selfplay
USER selfplay
ENV PATH="/home/selfplay/.local/bin:${PATH}"
WORKDIR /app


COPY --chown=selfplay:selfplay ./app/requirements.txt /app
RUN pip3 install -r /app/requirements.txt

COPY --chown=selfplay:selfplay ./app .

CMD bash
