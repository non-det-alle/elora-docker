# Ubuntu 22.04 (jammy)
# https://hub.docker.com/_/ubuntu/tags?page=1&name=jammy
ARG ROOT_CONTAINER=ubuntu:22.04

FROM $ROOT_CONTAINER

LABEL maintainer="Alessandro Aimi <alleaimi95@gmail.com>"
LABEL Description="Docker image for the ELoRa network emulator"

# Fix: https://github.com/hadolint/hadolint/wiki/DL4006
# Fix: https://github.com/koalaman/shellcheck/wiki/SC3014
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies 
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    # - apt-get upgrade is run to patch known vulnerabilities in apt-get packages as
    #   the ubuntu base image is rebuilt too seldom sometimes (less than once a month)
    apt-get upgrade --yes && \
    apt-get install --yes --no-install-recommends \
    ca-certificates \
    locales \
    # - tini is installed as a helpful container entrypoint that reaps zombie
    #   processes and such of the actual executable we want to start, see
    #   https://github.com/krallin/tini#why-tini for details.
    tini \
    wget \
    # Common useful utilities
    less \
    nano-tiny \
    tzdata \
    htop \
    ### Install OS dependences needed by Ns-3 ###
    g++ \
    python3 \
    cmake \
    ninja-build \
    git \
    # Optional for build optimization
    ccache \
    libcurl4-gnutls-dev \
    libboost-math-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Configure environment
ENV SHELL=/bin/bash \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV HOME="/home/elora" \
    # Bin directory
    PATH="/home/elora/.bin:${PATH}" \
    # Ns-3 directory
    NS3DIR="/home/elora/ns-3-dev"

# Create alternative for nano -> nano-tiny
RUN update-alternatives --install /usr/bin/nano nano /bin/nano-tiny 10

################################################################### HOME DIR

# Setup bin directories
RUN mkdir "${HOME}" "${HOME}/.bin"

WORKDIR "${HOME}"

# Install ns-3 with curl support and elora, and build
RUN git clone https://gitlab.com/non-det-alle/ns-3-dev.git && \
    cd ns-3-dev/contrib && \
    git clone https://github.com/non-det-alle/lorawan.git && \
    cd .. && \
    ./ns3 configure -d debug --enable-examples --enable-tests && \
    ./ns3 build && \
    cd ..

# Copy local files as late as possible to avoid cache busting
COPY ns3 ${HOME}/.bin/
# Import useful bash configuration
COPY .bashrc ${HOME}/

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["bash"]
