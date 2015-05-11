#include <stdlib.h>

int main(int argc, char **argv) {
    void *ptr = NULL;
    if (argc > 99) {
        ptr = malloc(sizeof(int));
    }
    int *x = (int *) ptr;
    if (x) {
        *x = 3;
    }
    return 0;
}
