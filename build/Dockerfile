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
    # Required by elora
    libcurl4-gnutls-dev \
    python3-toml && \
    # Cleanup
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Configure environment
ENV HOME="/home/elora" \
    # Ns-3 directory
    NS3DIR="/home/elora/ns-3-dev" \
    # Output directory
    OUTPUT="/home/elora/data"

# Install ns-3 with curl support and elora, and build
COPY ns-3-dev ${NS3DIR}
COPY lorawan ${NS3DIR}/src/lorawan
# Configure ns-3 to only build lorawan and dependencies to save disk space
RUN ${NS3DIR}/./ns3 configure \
    -d optimized \
    --enable-logs \ 
    --disable-warnings \
    --enable-modules lorawan && \
    # Build ns3
    ${NS3DIR}/./ns3 build && \
    # Setup home, data, and elora directories
    mkdir -p "${HOME}/data" "${NS3DIR}/scratch/elora"

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start.py"]

# Copy pther files as late as possible to avoid cache busting
COPY start.py /usr/local/bin/
