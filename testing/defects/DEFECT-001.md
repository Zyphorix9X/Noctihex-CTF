# TLS hostname field absent

Original certificate had no Subject Alternative Name. Replacement certificate includes three local identities and matches the preserved key. The user restarted Nginx; their integration test and the assistant's repeat both passed verified HTTPS. This defect is FIXED AND RETESTED. Earlier migration player tests used an exact certificate pin and remain separately identified.
