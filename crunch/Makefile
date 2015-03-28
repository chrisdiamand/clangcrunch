
.PHONY: all clean

SUBDIRS := \
    libcxxfileno \
    libsrk31cxx \
    libcxxgen \
    libdwarfpp \
    dwarfidl \
    liballocs \
    libcrunch

all: libcrunch_build

clean: $(SUBDIRS:%=%_clean)

libsrk31cxx_build: libcxxfileno_build

libdwarfpp_build: libsrk31cxx_build libcxxfileno_build libdwarf

libcxxgen_build: libdwarfpp_build

dwarfidl_build: antlr libdwarf libcxxgen_build libdwarfpp_build

liballocs_build: libcxxgen_build cil \
                 libdwarfpp_build dwarfidl_build

libcrunch_build: liballocs_build libcxxgen_build \
                 libdwarfpp_build dwarfidl_build

### Fetching and building ANTLR ###

ANTLR_TARGZ := antlr-3.4.tar.gz
ANTLR_URL := http://www.antlr3.org/download/antlr-3.4.tar.gz
ANTLR_DIR := antlr-3.4
ANTLR_JAR := antlr-3.4/lib/antlr-3.4-complete.jar
ANTLR_RUNTIME_DIR := antlr-3.4/runtime/C/dist/libantlr3c-3.4
ANTLR_RUNTIME := $(ANTLR_RUNTIME_DIR)/.libs/libantlr3c.so

$(ANTLR_TARGZ):
	wget $(ANTLR_URL)
	md5sum -c MD5SUM_antlr

# We just need to untar the archive
$(ANTLR_JAR): $(ANTLR_DIR)

$(ANTLR_RUNTIME_DIR).tar.gz: $(ANTLR_DIR)

$(ANTLR_RUNTIME_DIR)/Makefile: | $(ANTLR_RUNTIME_DIR)
	cd $(ANTLR_RUNTIME_DIR) && ./configure --enable-64bit

$(ANTLR_RUNTIME): $(ANTLR_RUNTIME_DIR)/Makefile
	$(MAKE) -C $(ANTLR_RUNTIME_DIR)

.PHONY: antlr
antlr: $(ANTLR_JAR) $(ANTLR_RUNTIME)

antlr_clean:
	rm -Rf $(ANTLR_DIR) # $(ANTLR_TARGZ)

# The tar.gz is always newer than its contents, so without the '|' this target
# gets rebuilt every time.
%: | %.tar.gz
	tar zxf $| -C $(shell dirname $|)
	[ -e $@ ] || echo "Warning: $@ not created"

### Fetching and building CIL ###

CIL_DIR := cil-git
CIL_REMOTE := git://git.code.sf.net/p/cil/code
CIL_MAKEFILE := $(CIL_DIR)/Makefile
CIL_BUILT := $(CIL_DIR)/bin/cilly

$(CIL_DIR):
	git clone $(CIL_REMOTE) $(CIL_DIR)

$(CIL_MAKEFILE): | $(CIL_DIR)
	cd $(CIL_DIR) && ./configure

$(CIL_BUILT): | $(CIL_MAKEFILE) $(CIL_DIR)
	$(MAKE) -C $(CIL_DIR)

.PHONY: cil
cil: $(CIL_BUILT)

### Fetching and building libdwarf (debian version is too old) ###
LIBDWARF_TARGZ := libdwarf-20150310.tar.gz
LIBDWARF_URL := http://www.prevanders.net/$(LIBDWARF_TARGZ)
LIBDWARF_DIR := dwarf-20150310
LIBDWARF_MAKEFILE := $(LIBDWARF_DIR)/Makefile
LIBDWARF_BUILT := $(LIBDWARF_DIR)/dwarfdump/dwarfdump

$(LIBDWARF_TARGZ):
	wget $(LIBDWARF_URL)
	md5sum -c MD5SUM_libdwarf

$(LIBDWARF_DIR): | $(LIBDWARF_TARGZ)
	tar zxvf $(LIBDWARF_TARGZ)

$(LIBDWARF_MAKEFILE): | $(LIBDWARF_DIR)
	cd $(LIBDWARF_DIR) && ./configure

$(LIBDWARF_BUILT): | $(LIBDWARF_MAKEFILE) $(LIBDWARF_DIR)
	$(MAKE) -C $(LIBDWARF_DIR)

.PHONY: libdwarf
libdwarf: $(LIBDWARF_BUILT)

%_build:
	$(MAKE) -C $*

%_clean:
	$(MAKE) -C $* clean
