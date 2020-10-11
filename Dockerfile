FROM python:alpine3.11
# Add python/pip build deps due to alpine
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Add bash
RUN apk add --no-cache --upgrade bash

# Arg values aren't avail after buildtime. Persist using ENV.
ARG COMMIT_SHA8="N/A"
ENV COMMIT_SHA8=$COMMIT_SHA8

COPY . /app

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/local/lib/python3.8/site-packages
RUN patch -p1 -i /app/libcloud_gce_resume_suspend.patch

WORKDIR /app
ENTRYPOINT ["/app/entrypoint.sh"]
