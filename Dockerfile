FROM python:alpine3.11
# Add python/pip build deps due to alpine
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Add bash
RUN apk add --no-cache --upgrade bash

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]
