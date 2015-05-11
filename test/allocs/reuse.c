#ifndef _GNU_SOURCE
    #define _GNU_SOURCE
#endif

#include <assert.h>
#include <stdlib.h>
#include <liballocs.h>

size_t global_size = 0;

int main(int argc, char **argv) {
    struct uniqtype *double_type = dlsym(RTLD_NEXT, "__uniqtype__double");
    assert(double_type != NULL);
    struct uniqtype *int_type = dlsym(RTLD_NEXT, "__uniqtype__int");
    assert(int_type != NULL);

    size_t size = (argc + 10) * sizeof(double);

    double *alloc1 = malloc(size);

    struct uniqtype *got_type = __liballocs_get_alloc_type(alloc1);
    assert(got_type != NULL);
    assert(got_type == double_type);

    size = sizeof(int) * 4;
    int *alloc2 = malloc(size);

    got_type = __liballocs_get_alloc_type(alloc2);
    assert(got_type != NULL);
    assert(got_type == int_type);

    // Also check globals

    global_size = sizeof(double);
    alloc1 = malloc(global_size);

    got_type = __liballocs_get_alloc_type(alloc1);
    assert(got_type != NULL);
    assert(got_type == double_type);

    global_size = sizeof(int);
    alloc2 = malloc(global_size);

    got_type = __liballocs_get_alloc_type(alloc2);
    assert(got_type != NULL);
    assert(got_type == int_type);

    *alloc2 = 3;

    return 0;
}
