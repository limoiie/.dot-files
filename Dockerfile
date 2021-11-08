ARG UBUNTU_VERSION=18.04
ARG SETUP=/tmp/setup-env.sh

FROM ubuntu:${UBUNTU_VERSION}
ENV LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8
ARG SETUP
COPY setup-env-install-dist-tools.sh /tmp/
RUN bash /tmp/setup-env-install-dist-tools.sh \
    && apt-get autoremove \
    && apt-get autoclean \
    && apt-get clean
COPY setup-env-install-modern-tools.sh /tmp/
RUN bash /tmp/setup-env-install-modern-tools.sh
COPY setup-env-config.sh /tmp/
RUN bash /tmp/setup-env-config.sh
WORKDIR /root
ENTRYPOINT [ "/bin/zsh" ]
