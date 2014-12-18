#!/usr/bin/env bash

export SRK31_PROJECTS=`realpath ~/src/srk31`

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
add_incl_path $SRK31_PROJECTS/liballocs/include
add_incl_path $SRK31_PROJECTS/liballocs/src
add_link_path $SRK31_PROJECTS/liballocs/lib
add_path_to_list PYTHONPATH $LIBALLOCS/tools/lang/c/lib

export ANTLR_M4_PATH=$SRK31_PROJECTS/m4ntlr

# ANTLR3. Use the version from here:
# http://www.antlr3.org/download/antlr-3.4.tar.gz

export ANTLR_SRC_PATH=`realpath ~/src/antlr-3.4`
add_incl_path $ANTLR_SRC_PATH/runtime/C/dist/libantlr3c-3.4
add_incl_path $ANTLR_SRC_PATH/runtime/C/dist/libantlr3c-3.4/include
add_link_path $ANTLR_SRC_PATH/runtime/C/dist/libantlr3c-3.4/.libs
add_class_path $ANTLR_SRC_PATH/lib/antlr-3.4-complete.jar
export ANTLR="java org.antlr.Tool"

# The CIL compiler wrapper uses this to store something, but defaults to
# /usr/allocsites for some reason.
export ALLOCSITES_BASE=/tmp/allocsites
