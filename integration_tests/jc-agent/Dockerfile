# Must be run in interactive mode to activate;
# Recommended run method:
# docker run -dit --env JC_CONNECT_KEY=<your-connect-key-here> <container-reference-here>
FROM ubuntu:20.04

LABEL maintainer="github.com/cascadianblue"

ARG version
RUN test -n "${version}"

ENV version=${version}
LABEL version=${version}
LABEL about.license="SPDX:Apache-2.0"

# Install dependencies
RUN apt-get update -qq -y && apt-get install --no-install-recommends -qq -y \
        apt-transport-https \
        curl \
        ca-certificates \
    && update-ca-certificates \
    && apt-get -y autoclean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# Kludgily install apt-show-versions
RUN rm /etc/apt/apt.conf.d/docker-gzip-indexes \
    && apt-get -o Acquire::GzipIndexes=false update \
    && apt-get install -y apt-show-versions

CMD curl --tlsv1.2 --silent --show-error --header "x-connect-key: ${JC_CONNECT_KEY}" https://kickstart.jumpcloud.com/Kickstart | bash; bash
