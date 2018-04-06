# This is a sample Dockerfile you can modify to deploy your own app

FROM python:3.6-slim

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

COPY . /root/rl_test
RUN cd /root/rl_test && \
    pip3 install -r requirements.txt

RUN echo 'deb http://www.deb-multimedia.org jessie main non-free' >> /etc/apt/sources.list \
    && echo 'deb-src http://www.deb-multimedia.org jessie main non-free' >> /etc/apt/sources.list \
    && apt-get --yes --force-yes update \
    && apt-get --yes --force-yes install deb-multimedia-keyring \
    && apt-get --yes --force-yes update

CMD cd /root/rl_test && \
    pytest test_install.py -svl --html=out.html

