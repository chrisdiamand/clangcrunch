#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <liballocs.h>

struct blah {
    int x;
    float y;
    char z[1];
};

int main(void) {
    void *b = calloc(1, offsetof(struct blah, z) + 10);

    struct uniqtype *got_type = __liballocs_get_alloc_type(b);
    struct uniqtype *blah_type = dlsym(RTLD_NEXT, "__uniqtype__blah");
    assert(blah_type);
    assert(got_type);
    assert(got_type == blah_type);

    printf("b->y = %f\n", ((struct blah *) b)->y);

    return 0;
}
