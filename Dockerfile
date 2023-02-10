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
    tzdata \
    # - tini is installed as a helpful container entrypoint that reaps zombie
    #   processes and such of the actual executable we want to start, see
    #   https://github.com/krallin/tini#why-tini for details.
    tini \
    ### Install OS dependences needed by Ns-3 ###
    g++ \
    python3 \
    cmake \
    ninja-build \
    git \
    # Optional for build optimization
    ccache \
    # Required by elora
    libcurl4-gnutls-dev \
    libboost-math-dev \
    python3-toml && \
    # Cleanup
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure environment
ENV HOME="/home/elora" \
    # Ns-3 directory
    NS3DIR="/home/elora/ns-3-dev" \
    # Output directory
    OUTPUT="/home/elora/data"

################################################################### HOME DIR

WORKDIR "${HOME}"

# Install ns-3 with curl support and elora, and build
RUN git clone https://gitlab.com/non-det-alle/ns-3-dev.git && \
    cd ns-3-dev/src && \
    git clone https://github.com/non-det-alle/lorawan.git && \
    cd .. && \
    ./ns3 configure -d optimized --enable-logs --disable-warnings --enable-modules lorawan && \
    ./ns3 build && \
    cd ..

# Setup home, data, and elora directories
RUN mkdir -p "${HOME}/data" \
    "${NS3DIR}/scratch/elora"

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start.py"]

# Copy local files as late as possible to avoid cache busting
COPY start.py /usr/local/bin/
