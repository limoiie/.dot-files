ARG UBUNTU_VERSION=18.04

FROM ubuntu:${UBUNTU_VERSION}
ENV LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8
RUN apt-get -o Acquire::http::proxy=false update \
    && apt-get install -o Acquire::http::proxy=false curl -y -q \
    && curl -o /tmp/setup-env.sh \
    -fsSL https://raw.githubusercontent.com/limoiie/.dot-files/master/setup-env.sh
RUN bash /tmp/setup-env.sh 1000 \
    && apt-get autoremove \
    && apt-get autoclean \
    && apt-get clean
RUN bash /tmp/setup-env.sh 0100
RUN bash /tmp/setup-env.sh 0011
WORKDIR /root
ENTRYPOINT [ "/bin/zsh" ]
