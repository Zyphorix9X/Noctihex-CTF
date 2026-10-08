#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define BASE "/opt/noctihex/backups/"

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        fprintf(stderr, "usage: nocti-backup <path>\n");
        return 1;
    }

    /*
     * Intentionally vulnerable CTF logic.
     * It only checks the text prefix and does not
     * properly resolve the final path first.
     */

    if (strncmp(argv[1], BASE, strlen(BASE)) != 0)
    {
        fprintf(stderr, "path not allowed\n");
        return 1;
    }

    execl(
        "/bin/cat",
        "cat",
        argv[1],
        (char *)NULL
    );

    return 1;
}