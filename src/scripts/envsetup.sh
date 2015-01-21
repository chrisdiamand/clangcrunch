#!/usr/bin/env bash

function add_link_path {
    add_path_to_list LD_LIBRARY_PATH $1
    add_path_to_list LIBRARY_PATH $1 \
        || echo "Error: '$1': Not a directory."
}

function add_incl_path {
    add_path_to_list CPATH $1 \
        || echo "Error: '$1': Not a directory."
}

function add_class_path {
    add_path_to_list CLASSPATH $1 \
        || echo "Error: '$1': Not a directory."
}

function add_bin_path {
    add_path_to_list PATH $1 \
        || echo "Error: '$1': Not a directory."
}

SCRIPT_DIR=`dirname $0`
SCRIPT_DIR=`realpath $SCRIPT_DIR`

source $SCRIPT_DIR/libcrunch_envsetup.sh
source $SCRIPT_DIR/clang_envsetup.sh
source $SCRIPT_DIR/utils_envsetup.sh
