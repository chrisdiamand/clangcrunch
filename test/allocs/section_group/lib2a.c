#define _GNU_SOURCE
#include <dlfcn.h>
#include "liballocs.h"

#include "section_group_uniqtype.h"

struct s2a
{
	int x;
} s;

void *l2a(void)
{
	/* Get our __uniqtype__s2a. */
	struct uniqtype *resolved = dlsym(__liballocs_my_typeobj(), "__uniqtype__s2a");
	/* Return our __uniqtype__int$32. */
	return resolved->contained[0].ptr;
}
