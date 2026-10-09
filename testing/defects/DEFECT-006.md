# Recovery HTTP port occupied — fixed and retested

The user supplied the Docker startup output: binding 127.0.0.1:8080 failed
because another listener already occupied that port. This happened while starting
the separate recovery Nginx container; primary validation had passed.

Removed the unused recovery HTTP port publication. All recovery helpers use verified
HTTPS on 8443, and SSH uses 2226. The corrected combined Compose configuration
passes `config --quiet`. The resumed completion run restored the backup successfully, passed 59 recovered
player checks and seven final integration checks. Status: FIXED AND RETESTED.
