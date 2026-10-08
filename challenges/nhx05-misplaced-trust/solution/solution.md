# NHX-05 – Misplaced Trust: Solution and Testing

## 1. Challenge Information

- **Category:** Linux / System Security
- **Difficulty:** Moderate–Hard
- **Points:** 300
- **Environment:** Ubuntu Docker container

## 2. SSH Connection Test

Connected to the local NHX-05 container using:

`ssh analyst@127.0.0.1 -p 2225`

**Result:** SSH connection successful.

## 3. User Verification

Command: `whoami`

Output: `analyst`

**Result:** Successfully logged in as a non-root user.

## 4. Sudo Permission Test

Command: `sudo -l`

Output:

`(root) NOPASSWD: /usr/local/bin/nocti-backup`

**Result:** The analyst user has permission to run the custom backup utility as root.

## 5. Normal Backup Test

Command:

`sudo /usr/local/bin/nocti-backup /opt/noctihex/backups/readme.txt`

Output:

`Nightly backup archive.`

**Result:** Normal backup operation successful.

## 6. Protected File Access Test

Command: `cat /root/flag.txt`

Output: `Permission denied`

**Result:** Direct access to the protected challenge file was blocked.

## 7. Intended Vulnerability Test

The backup utility performs an insufficient path validation check. Testing in the isolated challenge container confirmed that the intended path-validation weakness allows access to the fictional protected challenge file.

Recovered development values:

- Flag: `NOCTIHEX{DEV_NHX05}`
- Evidence: `DEV_E5`

**Result:** Intended challenge solution successful.

## 8. Test Summary

| Test | Status |
|---|---|
| SSH connection | PASS |
| Non-root user verification | PASS |
| Sudo permission verification | PASS |
| Normal backup operation | PASS |
| Direct protected file access blocked | PASS |
| Intended challenge solution | PASS |
| Development flag retrieval | PASS |

## 9. Reset

To recreate the local challenge environment, run from the project root:

`docker compose up -d --build --force-recreate nhx05`

Recheck SSH authentication, user permissions, and the normal backup operation afterward.

## 10. Conclusion

NHX-05 successfully demonstrated its intended Linux security training scenario in an isolated Docker environment. Further unintended-solution checks and final integration testing are required before submission.
