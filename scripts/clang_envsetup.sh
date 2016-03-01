LLVM_SOURCE=`readlink -m $SCRIPT_DIR/../external/llvm`
CLANG_SOURCE=`realpath -m $SCRIPT_DIR/../external/clang`

add_bin_path $LLVM_SOURCE/build-x86/bin
add_link_path $LLVM_SOURCE/build-x86/lib

CLANG_SYMLINK="$LLVM_SOURCE/tools/clang"

if [[ -e "$CLANG_SYMLINK" && ! -L "$CLANG_SYMLINK" ]]; then
    echo "Warning: $CLANG_SYMLINK is not a symlink to $CLANG_SOURCE"
else
    rm -f "$CLANG_SYMLINK"
    ln -s -T "$CLANG_SOURCE" "$CLANG_SYMLINK"
fi

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
