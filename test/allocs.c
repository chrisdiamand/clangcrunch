#include <stdlib.h>

int main(void) {
    int *x = malloc(sizeof(int) * 3);
    long *lp = (long *) x;
    return 0;
}
