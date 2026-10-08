#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

static uint32_t rotl32(uint32_t x, unsigned n) {
    return (x << n) | (x >> (32 - n));
}

static uint32_t nocti_check(const char *s) {
    uint32_t acc = 0x3132u;

    for (size_t i = 0; s[i] != '\0'; i++) {
        acc = rotl32(acc, 5) ^ (uint8_t)s[i];
        acc += (uint32_t)(i * 17u);
    }

    return acc;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: ./nocticore <evidence-chain>\n");
        return 1;
    }

    uint32_t result = nocti_check(argv[1]);

   printf("NoctiCore verification\n");

const uint32_t expected_check = 0xdc071061u;

if (result == expected_check) {
    printf("Evidence verification: SUCCESS\n");
    printf("NoctiCore unlocked.\n");

    unsigned char encoded_flag[] = {
        0x14, 0x15, 0x19, 0x0e, 0x13,
        0x12, 0x1f, 0x02, 0x21, 0x1e,
        0x1f, 0x0c, 0x05, 0x14, 0x12,
        0x02, 0x6a, 0x6c, 0x27
    };

    printf("Flag: ");

    for (size_t i = 0; i < sizeof(encoded_flag); i++) {
        putchar(encoded_flag[i] ^ 0x5A);
    }

    putchar('\n');
} else {
    printf("Evidence verification: FAILED\n");
    printf("Incorrect evidence chain.\n");
    return 1;
}

return 0;
}
