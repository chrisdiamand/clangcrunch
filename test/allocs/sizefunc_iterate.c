#ifndef _GNU_SOURCE
    #define _GNU_SOURCE
#endif

#include <assert.h>
#include <stdlib.h>
#include <liballocs.h>

size_t getsize();
size_t getsize2();

int main(void) {
    struct uniqtype *actual_type = dlsym(RTLD_NEXT, "__uniqtype__double");

    double *alloc1 = malloc(getsize());
    assert(alloc1 != NULL);

    struct uniqtype *got_type1 = __liballocs_get_alloc_type(alloc1);
    assert(actual_type != NULL);
    assert(got_type1 != NULL);
    assert(got_type1 == actual_type);

    // Check that normal allocations still work too.
    void *alloc3 = malloc(sizeof(int));
    struct uniqtype *int_type = dlsym(RTLD_NEXT, "__uniqtype__int");
    struct uniqtype *got_type3 = __liballocs_get_alloc_type(alloc3);
    assert(got_type3 != NULL);
    assert(got_type3 == int_type);
    return 0;
}

size_t getsize() {
    return 10 * getsize2();
}

size_t getsize2() {
    return sizeof(double);
}
