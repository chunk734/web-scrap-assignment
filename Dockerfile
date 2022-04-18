FROM ubuntu:20.04
SHELL	["/bin/bash"]

COPY ./etc	/etc

RUN	apt-get update; \
            apt-get install -yq python3.8 python3-pip; \
	pip3 install --upgrade --no-cache-dir  -r /etc/requirements.txt; \
    alias python="python3"

COPY ./src	/opt
