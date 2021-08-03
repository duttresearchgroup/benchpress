FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    wget \
    sudo \
    curl \
    python3 \
    python3-pip \
    git \
    libaio-dev \
    autoconf

RUN pip3 install PyYAML
RUN mkdir -p /workspace

## GNU time
RUN wget https://ftp.gnu.org/gnu/time/time-1.9.tar.gz && \
        tar -xzvf time-1.9.tar.gz && \
        cd time-1.9 && \
        ./configure --prefix=/usr && \
        make && \
        make install
	
WORKDIR /workspace/fbkutils/benchpress

CMD [ "bash" ]
