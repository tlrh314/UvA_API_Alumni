# syntax = docker/dockerfile:experimental
FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1

LABEL maintainer="Timo Halbesma <timo@halbesma.com>"

# Install system packages
WORKDIR /app
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,mode=0755,target=/var/cache/apt --mount=type=cache,mode=0755,target=/var/lib/apt set -ex \
    && apt-get update \
\
    # Install Build/Runtime dependencies ...
    && apt-get install -y --no-install-recommends \
\
        # ... a compiler (build)
        build-essential gcc \
        # ... for a proper editor (runtime)
        vim \
        # ... for the healthcheck (runtime)
        curl \
        # ... for monitoring (runtime)
        htop \
        # ... for Django translations (runtime)
        gettext \
        # ... for internal routing of uWSGI (runtime)
        libpcre3 libpcre3-dev \
        # ... for communication with the database (runtime)
        mariadb-client libmariadb-dev-compat \
\
    # Create apiweb user to run uWSGI as non-root
    && groupadd -g 1000 apiweb \
    && useradd -r -u 1000 -g apiweb apiweb -s /bin/bash -d /app

# Install python packages for Django
COPY requirements.txt /app/apiweb/requirements.txt
RUN --mount=type=cache,mode=0755,target=/root/.cache/pip set -ex && \
    pip install --upgrade pip \
    && pip install --upgrade pip \
    && pip install -r /app/apiweb/requirements.txt \
    && pip install mysqlclient uwsgi

# NB, we link the repo at runtime (which 'overwrites' files copied in on build)
# But production (when we run from image without linking the repo in) does use
# the files copied in!
COPY apiweb /app/apiweb
COPY uwsgi /app/uwsgi
COPY manage.py /app/manage.py
COPY entrypoint.sh /app/entrypoint.sh

RUN chown -R apiweb:apiweb /app

USER apiweb

ENTRYPOINT ["/app/entrypoint.sh"]
