THIS_DIR := $(realpath $(dir $(abspath "$(lastword $(MAKEFILE_LIST))" )))

ifeq ($(CC),cc)
    CC = allocscc
endif

LDFLAGS += -L$(THIS_DIR) -Wl,-R$(THIS_DIR)

CFLAGS += -g3 -gstrict-dwarf -std=c99 -fno-eliminate-unused-debug-types \
          -O2 -DUSE_STARTUP_BRK -I$(realpath $(LIBALLOCS)/include)
CFLAGS += -g3 -gstrict-dwarf -std=c99 -fno-eliminate-unused-debug-types \
          -O2 -DUSE_STARTUP_BRK -I$(realpath $(LIBALLOCS)/include)
CFLAGS += -fPIC -I$(realpath $(LIBALLOCS)/include)

OUT := section_group

.PHONY: all
all:
	$(MAKE) clean
	$(MAKE) $(OUT)

$(OUT): section_group.c lib1.so lib2.so
	$(CC) $(CFLAGS) $(LDFLAGS) $< lib1.so lib2.so -l1 -l2 -o $(OUT)

%.so: %.c %a.c
	$(CC) $(CFLAGS) -shared -o "$@" $^ $(LDFLAGS)

clean:
	rm -f lib1.so lib2.so $(OUT)
	rm -f *.fixuplog *.o *.allocstubs.* *.cil.* *.i.allocs *.i
