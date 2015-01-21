
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

libdwarfpp_build: libsrk31cxx_build libcxxfileno_build

libcxxgen_build: libdwarfpp_build

liballocs_build: liballocs_build libcxxgen_build \
                 libdwarfpp_build dwarfidl_build

libcrunch_build: liballocs_build libcxxgen_build \
                 libdwarfpp_build dwarfidl_build

%_build:
	$(MAKE) -C $*

%_clean:
	$(MAKE) -C $* clean
