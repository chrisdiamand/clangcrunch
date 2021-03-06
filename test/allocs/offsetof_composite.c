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

struct baz {
    void *a;
    struct blah b[1];
};

int main(void) {
    void *bz = calloc(1, offsetof(struct baz, b) + 20 * sizeof(struct blah));

    struct uniqtype *blah_type = dlsym(RTLD_NEXT, "__uniqtype__blah");
    assert(blah_type);

    struct uniqtype *got_comp_type = __liballocs_get_alloc_type(bz);
    struct uniqtype *baz_type = dlsym(RTLD_NEXT, "__uniqtype__baz");
    assert(baz_type);
    assert(got_comp_type);
    assert(got_comp_type->nmemb == 2);
    assert(got_comp_type->contained[0].ptr == baz_type);
    assert(got_comp_type->contained[1].ptr->is_array);
    assert(got_comp_type->contained[1].ptr->contained[0].ptr == blah_type);

    printf("bz->a = %p\n", ((struct baz *) bz)->a);
    struct blah useBlah;
    useBlah.y = 3.1415926;

    return 0;
}
