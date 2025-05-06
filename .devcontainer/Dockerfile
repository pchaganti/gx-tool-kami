FROM ubuntu:24.04

RUN apt-get update && apt-get install -y \
    # Dev dependencies
    git git-lfs curl libssl-dev libreadline-dev zlib1g-dev autoconf bison build-essential libyaml-dev libreadline-dev libncurses5-dev libffi-dev libgdbm-dev \
    # Utils
    nfs-common iputils-ping sudo wget unzip \
    # GCloud
    apt-transport-https ca-certificates gnupg curl \
    && rm -rf /var/lib/apt/lists/*

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && apt-get update -y && apt-get install google-cloud-cli -y

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/