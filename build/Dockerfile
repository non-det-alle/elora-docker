# Alpine 3.17
# https://hub.docker.com/_/alpine/tags?page=1&name=3.17
FROM alpine:3.17

LABEL maintainer="Alessandro Aimi <alleaimi95@gmail.com>"
LABEL Description="Docker image for the ELoRa network emulator"

USER root

# Configure environment
ENV HOME="/home/elora" \
    # Ns-3 directory
    NS3DIR="/home/elora/ns-3-dev" \
    # Output directory
    OUTPUT="/home/elora/data"

# Copy ns-3 and elora emulator code
COPY ns-3-dev ${NS3DIR}
COPY elora ${NS3DIR}/contrib/lorawan

# Install OS dependencies, modified ns-3, and elora
RUN apk --no-cache add \
    ca-certificates \
    tzdata \
    linux-headers \
    # - tini is installed as a helpful container entrypoint that reaps zombie
    #   processes and such of the actual executable we want to start, see
    #   https://github.com/krallin/tini#why-tini for details.
    tini \
    # Dependences of ns-3
    g++ \
    cmake \
    ninja \
    python3 \
    # Required by elora
    patch \
    iptables \
    curl-dev \
    py3-toml && \
    # Apply patch to ns-3 to support libcurl
    patch -p1 -d ${NS3DIR} < ${NS3DIR}/contrib/lorawan/ns-3-dev.patch && \
    # Configure ns-3 to only build lorawan and dependencies to save disk space
    ${NS3DIR}/./ns3 configure \
        --build-profile optimized \
        --enable-modules lorawan \
        --disable-warnings && \
    # Build ns3
    ${NS3DIR}/./ns3 build && \
    # Setup home, data, ns-3-dev/scratch/elora-example directories
    mkdir -p "${HOME}/data" "${NS3DIR}/scratch/elora-example"

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start.py"]

# Copy other files as late as possible to avoid cache busting
COPY start.py /usr/local/bin/
