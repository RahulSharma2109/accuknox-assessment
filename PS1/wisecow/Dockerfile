FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/games:${PATH}"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        fortune-mod \
        fortunes \
        cowsay \
        netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

COPY wisecow.sh .

RUN chmod +x wisecow.sh

EXPOSE 4499

CMD ["./wisecow.sh"]
