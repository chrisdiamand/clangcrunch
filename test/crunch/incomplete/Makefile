OUT := incomplete

LIBCRUNCH = $(realpath $(LIBALLOCS)/../libcrunch)

ifeq ($(CC),cc)
    CC=crunchcc
endif

CFLAGS := -O0 -std=c99 -D_GNU_SOURCE -DUSE_STARTUP_BRK -I$(LIBCRUNCH)/include

.PHONY: all
all:
	$(MAKE) clean
	$(MAKE) $(OUT)

.PHONY: run
run:
	LD_PRELOAD=$(LIBCRUNCH)/lib/libcrunch_preload.so $(realpath $(OUT))

$(OUT): incomplete.o lib.o
	$(CC) -o "$@" $(CFLAGS) $+ $(LDFLAGS) $(LDLIBS)

clean:
	rm -f $(OUT) *.o *.cil.* *.i *.allocstubs.* *.fixuplog *.i.allocs
