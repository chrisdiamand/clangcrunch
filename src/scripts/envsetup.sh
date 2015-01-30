#!/usr/bin/env bash

function diss_add_path_to_list {
    VAR="$1"
    P=`realpath $2`
    eval CURVAL=\$$VAR
    if notin "$P" "$CURVAL"; then
        export $VAR=$P:$CURVAL
    fi
    if [ -d "`dirname $P`" ]; then
        return 0
    fi
    return 1 # Error if the path doesn't exist
}

function add_link_path {
    diss_add_path_to_list LD_LIBRARY_PATH $1
    diss_add_path_to_list LIBRARY_PATH $1 \
        || echo "Warning: '$1': Not a directory."
}

function add_incl_path {
    diss_add_path_to_list CPATH $1 \
        || echo "Warning: '$1': Not a directory."
}

function add_class_path {
    diss_add_path_to_list CLASSPATH $1 \
        || echo "Warning: '$1': Not a directory."
}

function add_bin_path {
    diss_add_path_to_list PATH $1 \
        || echo "Warning: '$1': Not a directory."
}

SCRIPT_DIR=`dirname $0`
SCRIPT_DIR=`realpath $SCRIPT_DIR`

source $SCRIPT_DIR/libcrunch_envsetup.sh
source $SCRIPT_DIR/clang_envsetup.sh
source $SCRIPT_DIR/utils_envsetup.sh
