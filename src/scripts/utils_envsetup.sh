function dump_ast {
    clang -Xclang -ast-dump $@
}
