ARG UBUNTU_VERSION=18.04

FROM ubuntu:${UBUNTU_VERSION}
ENV LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8
RUN apt-get -o Acquire::http::proxy=false update \
    && apt-get install -o Acquire::http::proxy=false curl -y -q \
    && curl -fsSL https://raw.githubusercontent.com/limoiie/.dot-files/master/setup-env.sh | bash -s -- -y \
    && apt-get autoclean \
    && apt-get clean
    ### disabled because: Cannot find Cargo.toml
    # && cargo clean --quiet \
    # && rm /root/.cargo/bin/cargo* \
    # && rm /root/.cargo/bin/rust* \
    # && rm /root/.cargo/bin/rls \
    # && rm /root/.cargo/bin/clippy-driver
WORKDIR /root
ENTRYPOINT [ "/bin/zsh" ]
