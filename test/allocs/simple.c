#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <liballocs.h>

struct foo {
    int x;
};

int main(void) {
    void *b = calloc(1, sizeof(struct foo));

    // assert that the alloc is a struct foo
    struct uniqtype *got_type = __liballocs_get_alloc_type(b);
    struct uniqtype *data_type = dlsym(RTLD_NEXT, "__uniqtype__foo");
    assert(data_type);
    assert(got_type);
    assert(got_type == data_type);

    // We need to use the struct or clang will remove the unused debug info.
    ((struct foo *) b)->x = 3;

    return 0;
}
