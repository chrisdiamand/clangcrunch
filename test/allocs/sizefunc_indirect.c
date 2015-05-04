#ifndef _GNU_SOURCE
    #define _GNU_SOURCE
#endif

#include <assert.h>
#include <stdlib.h>
#include <liballocs.h>

size_t getsize2() {
    return sizeof(double);
}

int main(void) {
    struct uniqtype *actual_type = dlsym(RTLD_NEXT, "__uniqtype__double");
    assert(actual_type != NULL);

    void *gs1 = getsize2;
    size_t (*gs2)(void) = getsize2;
    size_t indirect_size = gs2();

    double *alloc2 = malloc(indirect_size);
    assert(alloc2 != NULL);

    struct uniqtype *got_type2 = __liballocs_get_alloc_type(alloc2);
    assert(got_type2 != NULL);
    assert(got_type2 == actual_type);

    /* Weird bug: liballocs can't find the alloc size when it's allocated like
     * malloc(gs2()). The type is detected correctly though so the bug is in
     * liballocs. */

    // Check that normal allocations still work.
    void *alloc3 = malloc(sizeof(int));
    struct uniqtype *int_type = dlsym(RTLD_NEXT, "__uniqtype__int");
    struct uniqtype *got_type3 = __liballocs_get_alloc_type(alloc3);
    assert(got_type3 != NULL);
    assert(got_type3 == int_type);
    return 0;
}
