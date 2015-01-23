#include <stdio.h>
#include <stdint.h>

int __is_aU(void *p) {
    putchar(97);
    return 0;
}

int main(void) {
    long x;
    long *xp = &x;
    int *ip = (int *) xp;
    x = 123L;
    printf("*ip = %d\n", *ip);
    return 0;
}
