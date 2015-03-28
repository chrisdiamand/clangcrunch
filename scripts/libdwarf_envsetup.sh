LIBDWARF=`realpath $SCRIPT_DIR/../crunch/dwarf-20150310`

add_bin_path $LIBDWARF/dwarfdump
add_incl_path $LIBDWARF/libdwarf
add_link_path $LIBDWARF/libdwarf
