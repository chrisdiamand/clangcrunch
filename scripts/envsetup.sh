#!/usr/bin/env bash

# readlink that works everywhere
function crunch_realpath {
    python -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "$1"
}

if [ "$0" = "bash" -o "$0" = "-bash" ]; then
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
    SCRIPT_DIR=`dirname $0`
    SCRIPT_DIR=`crunch_realpath $SCRIPT_DIR`
fi

function diss_add_path_to_list {
    VAR="$1"
    P=`crunch_realpath $2`
    eval CURVAL=\$$VAR
    if notin "$P" "$CURVAL"; then
        export $VAR=$P:$CURVAL
    fi
    if [ -d "`dirname $P`" ]; then
        return 0
    fi
    return 1 # Error if the path doesn't exist
}

function warn_not_dir {
    echo "Warning: '`crunch_realpath $1`': Not a directory."
}

function add_link_path {
    diss_add_path_to_list LD_LIBRARY_PATH $1
    diss_add_path_to_list LIBRARY_PATH $1 || warn_not_dir $1
}

function add_incl_path {
    diss_add_path_to_list CPATH $1 || warn_not_dir $1
}

function add_class_path {
    diss_add_path_to_list CLASSPATH $1 || warn_not_dir $1
}

function add_bin_path {
    diss_add_path_to_list PATH $1 || warn_not_dir $1
}

function add_python_path {
    diss_add_path_to_list PYTHONPATH $1 || warn_not_dir $1
}

source $SCRIPT_DIR/libcrunch_envsetup.sh
source $SCRIPT_DIR/clang_envsetup.sh
source $SCRIPT_DIR/utils_envsetup.sh
#source $SCRIPT_DIR/libdwarf_envsetup.sh

add_bin_path $SCRIPT_DIR/../bin
add_python_path $SCRIPT_DIR/../lib
