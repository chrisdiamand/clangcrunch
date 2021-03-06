.PHONY: all clean

DEBUG ?= 1

PROJ_ROOT := $(realpath ../external)

PROJECTS_TO_CLEAN := \
    libcxxfileno \
    libsrk31cxx \
    libcxxgen \
    libdwarfpp \
    dwarfidl \
    liballocs \
    libcrunch

all: libcrunch_build

clean: $(PROJECTS:%=%_clean)

libsrk31cxx_build: libcxxfileno_build

libdwarfpp_build: libsrk31cxx_build libcxxfileno_build

libcxxgen_build: libdwarfpp_build

dwarfidl_build: antlr libcxxgen_build libdwarfpp_build

liballocs_build: libcxxgen_build cil \
                 libdwarfpp_build dwarfidl_build

libcrunch_build: liballocs_build libcxxgen_build \
                 libdwarfpp_build dwarfidl_build

### Fetching and building ANTLR ###

.PHONY: antlr
antlr:
	$(MAKE) -C antlr_build

antlr_clean:
	$(MAKE) -C antlr_build clean

# The tar.gz is always newer than its contents, so without the '|' this target
# gets rebuilt every time.
%: | %.tar.gz
	tar zxf $| -C $(shell dirname $|)
	[ -e $@ ] || echo "Warning: $@ not created"

### Fetching and building CIL ###

CIL_DIR := $(PROJ_ROOT)/cil
CIL_MAKEFILE := $(CIL_DIR)/Makefile
CIL_BUILT := $(CIL_DIR)/bin/cilly

$(CIL_MAKEFILE): | $(CIL_DIR)
	cd $(CIL_DIR) && ./configure

$(CIL_BUILT): | $(CIL_MAKEFILE) $(CIL_DIR)
	$(MAKE) -C $(CIL_DIR)

.PHONY: cil
cil: $(CIL_BUILT)

%_build:
	$(MAKE) -C $(PROJ_ROOT)/$* DEBUG=$(DEBUG)

# liballocs tests are broken, but get built by default, so specify the exact
# targets we need individually.
liballocs_build:
	$(MAKE) -C $(PROJ_ROOT)/liballocs DEBUG=$(DEBUG) tools
	$(MAKE) -C $(PROJ_ROOT)/liballocs DEBUG=$(DEBUG) src
	$(MAKE) -C $(PROJ_ROOT)/liballocs DEBUG=$(DEBUG) lib

%_clean:
	$(MAKE) -C $(PROJ_ROOT)/$* clean DEBUG=$(DEBUG)
