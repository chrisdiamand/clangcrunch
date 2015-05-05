#ifndef _GNU_SOURCE
    #define _GNU_SOURCE
#endif

#include <assert.h>
#include <stdlib.h>
#include <liballocs.h>

struct coord {
    int x;
    int y;
} coords[] = {{1, 2}, {3, 4}};

int main(void) {
    struct uniqtype *double_type = dlsym(RTLD_NEXT, "__uniqtype__double");
    assert(double_type != NULL);
    struct uniqtype *coord_type = dlsym(RTLD_NEXT, "__uniqtype__coord");
    assert(coord_type != NULL);

    double *alloc1 = malloc(sizeof(coords)/sizeof(*coords) * sizeof(double));

    struct uniqtype *got_type1 = __liballocs_get_alloc_type(alloc1);
    assert(got_type1 != NULL);
    assert(got_type1 == double_type);

    size_t size = sizeof(int) * sizeof(struct coord) + sizeof(double);
    struct coord *alloc2 = malloc((size - sizeof(double)) / sizeof(int));

    struct uniqtype *got_type2 = __liballocs_get_alloc_type(alloc2);
    assert(got_type2 != NULL);
    assert(got_type2 == coord_type);

    return 0;
}
