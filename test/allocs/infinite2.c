#include <stdlib.h>

size_t calcB();

size_t calcA() {
    return sizeof(int) + calcB();
}

size_t calcB() {
    return sizeof(int) + calcA();
}

int main(void) {
    malloc(calcA());
    return 0;
}
