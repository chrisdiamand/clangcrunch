#!/usr/bin/env bash

if [ "$0" = "bash" -o "$0" = "-bash" ]; then
    SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
else
    SCRIPT_DIR=`dirname $0`
    SCRIPT_DIR=`readlink -m $SCRIPT_DIR`
fi

function diss_add_path_to_list {
    function _diss_path_not_in_path_list {
        local p="$1"
        local plist="$2"
        if [[ "$plist" == "$p" ||
            "$plist" == "$p:"* ||
            "$plist" == *":$p:"* ||
            "$plist" == *":$p" ]]; then
            return 1
        fi
        return 0
    }

    local VAR="$1" P=`readlink -m $2` CURVAL= RET=0

    eval CURVAL=\$$VAR
    if _diss_path_not_in_path_list "$P" "$CURVAL"; then
        export $VAR=$P:$CURVAL
    fi

    [[ -d `dirname "$P"` ]] || RET=1

    unset -f _diss_path_not_in_path_list
    return "$RET"
}

function warn_not_dir {
    echo "Warning: '$1': Not a directory."
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
