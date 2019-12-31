#include <stdio.h>

ssize_t signum(ssize_t input) {
    printf("From shared library, I got input %ld\n", input);
    if (0 == input) {
        return 0;
    }
    return input < 0 ? -1 : 1;
}
