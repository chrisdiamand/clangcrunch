#ifndef _GNU_SOURCE
    #define _GNU_SOURCE
#endif

#include <assert.h>
#include <netinet/in.h>
#include <stdio.h>
#include <sys/socket.h>

#include "libcrunch.h"

void *test_void_ptr;
struct sockaddr test_sockaddr;

int main(void) {
    struct foo {
        int bar;
    } **blah = malloc(sizeof (void*));

    assert(__libcrunch_is_initialized);

    struct sockaddr_in *p_mysock = malloc(sizeof (struct sockaddr));

    fprintf(stderr, "Allocated a sockaddr_in at %p\n", p_mysock);

    // Use struct foo so that the types don't get eliminated.
    struct foo aFoo;
    struct foo *pFoo = &aFoo;

    return 0;
}
