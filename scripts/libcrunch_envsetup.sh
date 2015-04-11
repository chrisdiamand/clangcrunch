#!/usr/bin/env bash

export SRK31_PROJECTS=`crunch_realpath $SCRIPT_DIR/../..`

add_incl_path $SRK31_PROJECTS/libsrk31cxx/include
add_link_path $SRK31_PROJECTS/libsrk31cxx/lib

add_incl_path $SRK31_PROJECTS/libcxxfileno/include
add_link_path $SRK31_PROJECTS/libcxxfileno/lib

add_incl_path $SRK31_PROJECTS/libdwarfpp/include
add_link_path $SRK31_PROJECTS/libdwarfpp/lib

add_incl_path $SRK31_PROJECTS/dwarfidl/include
add_link_path $SRK31_PROJECTS/dwarfidl/lib

add_incl_path $SRK31_PROJECTS/libcxxgen/include
add_link_path $SRK31_PROJECTS/libcxxgen/lib

add_incl_path $SRK31_PROJECTS/libantlr3cxx/include

export LIBALLOCS=$SRK31_PROJECTS/liballocs
export LIBALLOCS_BASE=$LIBALLOCS
export ALLOCSITES_BASE=$SRK31_PROJECTS/allocsites
export UNIQTYPES_BASE=$ALLOCSITES_BASE
add_incl_path $LIBALLOCS/include
add_incl_path $LIBALLOCS/src
add_link_path $LIBALLOCS/lib
add_bin_path $LIBALLOCS/tools
add_bin_path $LIBALLOCS/tools/lang/c/bin
add_bin_path $LIBALLOCS/tools/lang/c++/bin
add_python_path $LIBALLOCS/tools/lang/c/lib
#export DEBUG_CC=1

export ANTLR_M4_PATH=$SRK31_PROJECTS/m4ntlr

# ANTLR3. Use the version from here:
# http://www.antlr3.org/download/antlr-3.4.tar.gz

export ANTLR_SRC_PATH=$SCRIPT_DIR/../build/antlr_build/antlr-3.4
add_incl_path $ANTLR_SRC_PATH/runtime/C/dist/libantlr3c-3.4
add_incl_path $ANTLR_SRC_PATH/runtime/C/dist/libantlr3c-3.4/include
add_link_path $ANTLR_SRC_PATH/runtime/C/dist/libantlr3c-3.4/.libs
add_class_path $ANTLR_SRC_PATH/lib/antlr-3.4-complete.jar
export ANTLR="java org.antlr.Tool"

add_link_path $SRK31_PROJECTS/libcrunch/lib
add_bin_path $SRK31_PROJECTS/libcrunch/frontend/c/bin

add_link_path $SRK31_PROJECTS/cil-git/lib
add_bin_path $SRK31_PROJECTS/cil-git/bin

function allocs_gdb {
    FNAME=/tmp/gdb_allocs_preload.txt
    echo "set env LD_PRELOAD $LIBALLOCS/src/liballocs_preload.so" > $FNAME
    gdb -command=$FNAME $@
    rm -f $FNAME
}

function crunch_gdb {
    FNAME=/tmp/gdb_crunch_preload.txt
    echo "set env LD_PRELOAD $SRK31_PROJECTS/libcrunch/src/libcrunch_preload.so" > $FNAME
    gdb -command=$FNAME $@
    rm -f $FNAME
}
