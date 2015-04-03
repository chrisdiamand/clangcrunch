### Fetching and building ANTLR ###

ANTLR_TARGZ := antlr-3.4.tar.gz
ANTLR_URL := http://www.antlr3.org/download/antlr-3.4.tar.gz
ANTLR_DIR := antlr-3.4
ANTLR_JAR := antlr-3.4/lib/antlr-3.4-complete.jar
ANTLR_RUNTIME_DIR := antlr-3.4/runtime/C/dist/libantlr3c-3.4
ANTLR_RUNTIME := $(ANTLR_RUNTIME_DIR)/.libs/libantlr3c.so

.PHONY: all
all: $(ANTLR_JAR) $(ANTLR_RUNTIME)

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

clean:
	rm -Rf $(ANTLR_DIR) # $(ANTLR_TARGZ)

# The tar.gz is always newer than its contents, so without the '|' this target
# gets rebuilt every time.
%: | %.tar.gz
	 tar zxf $| -C $(shell dirname $|)
	[ -e $@ ] || echo "Warning: $@ not created"
