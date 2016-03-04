clangcrunch
===========

This repository contains the 'clangcrunchcc' compiler wrapper, some tests, and
'envsetup.sh'.

Obtaining the source
====================

There are many dependencies though.

The easiest way to get everything is by cloning this repo and using git
submodules to get the dependencies:

    $ git clone https://github.com/chrisdiamand/clangcrunch.git
    $ cd clangcrunch
    $ git submodule update --init --recursive

Alternatively, download directly:

    $ git clone https://github.com/chrisdiamand/llvm.git
    $ cd llvm/tools/ && git clone https://github.com/chrisdiamand/clang.git
    # Forks of Stephen Kell's projects:
    $ git clone https://github.com/chrisdiamand/libcrunch.git
    $ git clone https://github.com/chrisdiamand/liballocs.git
    $ git clone https://github.com/chrisdiamand/dwarfidl.git
    $ git clone https://github.com/chrisdiamand/libdwarfpp.git

libcrunch has several other dependencies - these can be downloaded from
`https://github.com/stephenrkell`

As a last resort, patches containing the changes required for each project are
included in the patches/ directory.

Building
========

Build Stephen's projects
------------------------
    $ source scripts/envsetup.sh
    $ cd build
    $ make

Build Clang
-----------

    $ cd external/llvm
    # Create a link to the clang directory if necessary, although this should have
    # been done automatically by 'envsetup.sh'.
    $ ln -s -T ../clang tools/clang
    $ mkdir -p build-x86 && cd build-x86
    $ cmake -G Ninja ..
    $ ninja

Running
=======

    $ clangcrunchcc /my/source/program.c -o program
    $ LD_PRELOAD=/path/to/clangrunch/external/libcrunch/src/libcrunch_preload.so ./program
