#include <stdio.h>

int main(void) {
    long x;
    long *xp = &x;
    int *ip = (int *) xp;
    x = 123L;
    printf("*ip = %d\n", *ip);
    return 0;
}
