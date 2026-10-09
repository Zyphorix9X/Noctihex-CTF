#!/bin/bash

set -e

echo "${NHX05_FLAG}" > /root/flag.txt
echo "fragment=${NHX05_EVIDENCE}" >> /root/flag.txt

chmod 600 /root/flag.txt
unset NHX05_FLAG NHX05_EVIDENCE

echo "Nightly backup archive." \
    > /opt/noctihex/backups/readme.txt

mkdir -p /etc/ssh/hostkeys
if [ ! -f /etc/ssh/hostkeys/ssh_host_ed25519_key ]; then
    ssh-keygen -q -t ed25519 -N '' -f /etc/ssh/hostkeys/ssh_host_ed25519_key
fi
exec /usr/sbin/sshd -D -e -h /etc/ssh/hostkeys/ssh_host_ed25519_key
