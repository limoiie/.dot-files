ARG UBUNTU_VERSION=18.04
ARG SETUP=/tmp/setup-env.sh

FROM ubuntu:${UBUNTU_VERSION}
ENV LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8
ARG SETUP
COPY setup-env.sh ${SETUP}
RUN bash ${SETUP} 1000 \
    && apt-get autoremove \
    && apt-get autoclean \
    && apt-get clean
RUN bash ${SETUP} 0100
RUN bash ${SETUP} 0011
WORKDIR /root
ENTRYPOINT [ "/bin/zsh" ]
