#include <stdlib.h>

size_t calcB(void);
size_t calcC(void);

size_t calcA(void) {
    return sizeof(int) + calcB();
}

size_t calcB(void) {
    size_t (*indirect)(void);
    indirect = calcC;
    return sizeof(int) + indirect();
}

size_t valid(void) {
    return sizeof(double);
}

size_t calcC(void) {
    return valid() + calcC();
}

size_t shouldB(void);
size_t shouldC(void);

// This one changes multiple times, but isn't recursive.
size_t shouldA(void) { // 1st: int, 2nd: 2*int, 3rd: 3*int
    return sizeof(int) + shouldB();
}

size_t shouldB(void) { // 1st: int, 2nd: 2*int
    return sizeof(int) + shouldC();
}

size_t shouldC(void) { // 1st: int, 2nd: int
    return sizeof(int);
}


int main(void) {
    malloc(calcA());
    malloc(valid());
    malloc(shouldA());
    return 0;
}
