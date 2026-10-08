FROM ubuntu:24.04 AS builder

RUN apt-get update && \
    apt-get install -y gcc

WORKDIR /build

COPY nocti-backup.c .

RUN gcc nocti-backup.c -o nocti-backup


FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y \
        openssh-server \
        sudo && \
    rm -rf /var/lib/apt/lists/*

RUN useradd \
    -m \
    -s /bin/bash \
    analyst && \
    echo "analyst:nocti2026" | chpasswd

RUN mkdir -p \
    /run/sshd \
    /opt/noctihex/backups

COPY --from=builder \
    /build/nocti-backup \
    /usr/local/bin/nocti-backup

RUN chown root:root \
    /usr/local/bin/nocti-backup && \
    chmod 755 \
    /usr/local/bin/nocti-backup

RUN echo \
    'analyst ALL=(root) NOPASSWD: /usr/local/bin/nocti-backup' \
    > /etc/sudoers.d/noctihex && \
    chmod 440 \
    /etc/sudoers.d/noctihex

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 22

ENTRYPOINT ["/entrypoint.sh"]
