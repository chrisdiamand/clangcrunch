LLVM_SOURCE=`crunch_realpath $SCRIPT_DIR/../../llvm`

add_bin $LLVM_SOURCE/build/bin
add_lib $LLVM_SOURCE/build/lib

function cmake_crunchclang {
    DIR=$1
    if [ -z "$DIR" ]; then
        DIR=$LLVM_SOURCE
    fi

    CXX="ccache clang++ -Qunused-arguments -fcolor-diagnostics" \
    CC="ccache clang -Qunused-arguments -fcolor-diagnostics" \
    CCACHE_CPP2=yes \
    cmake -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=DEBUG $DIR
}
