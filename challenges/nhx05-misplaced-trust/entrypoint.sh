#!/bin/bash

set -e

echo "${NHX05_FLAG}" > /root/flag.txt
echo "fragment=${NHX05_EVIDENCE}" >> /root/flag.txt

chmod 600 /root/flag.txt

echo "Nightly backup archive." \
    > /opt/noctihex/backups/readme.txt

exec /usr/sbin/sshd -D -e