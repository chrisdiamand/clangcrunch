#ifndef _GNU_SOURCE
    #define _GNU_SOURCE
#endif

#include <assert.h>
#include <stdlib.h>
#include <liballocs.h>

size_t getsize() {
    return sizeof(double) * sizeof(int);
}

int main(void) {
    struct uniqtype *actual_type = dlsym(RTLD_NEXT, "__uniqtype__double");
    assert(actual_type != NULL);

    size_t size = sizeof(int) + getsize() + sizeof(int);
    double *alloc2 = malloc(size/sizeof(int));
    assert(alloc2 != NULL);

    struct uniqtype *got_type2 = __liballocs_get_alloc_type(alloc2);
    assert(got_type2 != NULL);
    assert(got_type2 == actual_type);

    double aDouble = 3.141;

    return 0;
}
