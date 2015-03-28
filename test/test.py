#!/usr/bin/env python3

from os import path
import os
import subprocess
import sys

if "LIBALLOCS_BASE" in os.environ:
    ALLOCSDIR = os.environ["LIBALLOCS_BASE"]
else:
    ALLOCSDIR = path.join(path.dirname(__file__), "../crunch/liballocs")
ALLOCSDIR = path.realpath(ALLOCSDIR)

TESTDIR = path.realpath(path.dirname(__file__))


CLEAN_EXTS = ["-allocsites.c", "-allocsites.so", "-types.c", "-types.c.log.gz",
              "-types.so", ".allocs", ".allocs.rej", ".allocstubs.c",
              ".allocstubs.i", ".allocstubs.o", ".cil.c", ".cil.i", ".cil.s",
              ".i", ".i.allocs", ".makelog", ".o", ".o.fixuplog", ".objallocs",
              ".s", ".srcallocs", ".srcallocs.rej"]

class Test:
    def run(self):
        self.clean()

        print(" ".join(self.buildCmd()))
        status = subprocess.call(self.buildCmd())
        if status != 0:
            return status

        env = dict(os.environ)
        liballocs = path.join(ALLOCSDIR, "lib/liballocs_preload.so")
        env["LD_PRELOAD"] = path.realpath(liballocs)
        print("LD_PRELOAD=" + env["LD_PRELOAD"] + " " +
              " ".join(self.runCmd()))
        proc = subprocess.Popen(self.runCmd(), env = env)
        return proc.wait()

    def cleanFiles(self):
        return []

    def clean(self):
        for f in self.getCleanFiles():
            if path.exists(f):
                print("Removing \'%s\'" % f)
                os.unlink(f)

class StockAllocsTest(Test):
    def __init__(self, fname):
        self.src_fname = fname
        self.out_fname = path.splitext(self.src_fname)[0] \
                       + "_" + self.getCompiler()

    def getCompiler(self):
        return "allocscc"

    def getName(self):
        return self.out_fname

    def buildCmd(self):
        cmd = [self.getCompiler()]
        cmd += ["-g3", "-gstrict-dwarf", "-std=c99",
                "-fno-eliminate-unused-debug-types",
                "-O2", "-DUSE_STARTUP_BRK",
                "-I" + ALLOCSDIR + "/include"]
        cmd += ["-std=c99", self.src_fname,
                "-o", self.out_fname]
        return cmd

    def runCmd(self):
        return ["./" + self.out_fname]

    def getCleanFiles(self):
        files = [self.out_fname + e for e in CLEAN_EXTS]
        files += [path.splitext(self.src_fname)[0] + e for e in CLEAN_EXTS]
        files += [self.out_fname]

        if "ALLOCSITES_BASE" in os.environ:
            sites = os.environ["ALLOCSITES_BASE"]
        else:
            sites = "/usr/lib/allocsites"
        sites = path.realpath(sites)
        sites = sites + path.realpath(self.out_fname)
        files += [sites + e for e in CLEAN_EXTS]

        return files

class AllocsTest(StockAllocsTest):
    def getCompiler(self):
        return "clang_allocscc"

def register_tests():
    tests = {}
    def add(t):
        assert isinstance(t, Test)
        tests[t.getName()] = t

    add(StockAllocsTest("allocs_simple.c"))
    add(AllocsTest("allocs_simple.c"))
    add(AllocsTest("allocs_offsetof_simple.c"))
    add(AllocsTest("allocs_offsetof_composite.c"))

    return tests

def main():
    tests = register_tests()

    if "zshcomp" in sys.argv:
        for t in tests:
            print(t)
        print("clean")
        return 0

    if "clean" in sys.argv:
        for t in tests:
            tests[t].clean()
        for f in os.listdir(TESTDIR):
            for e in CLEAN_EXTS:
                fullpath = path.join(TESTDIR, f)
                if fullpath.endswith(e) and path.exists(fullpath):
                    print("Removing \'%s\'" % fullpath)
                    os.unlink(fullpath)
        return 0

    testNames = sys.argv[1:]
    if len(testNames) == 0:
        testNames = list(tests.keys())

    nonexist = 0
    passed = 0
    failed = 0
    total = len(testNames)

    for tn in testNames:
        if tn in tests:
            if tests[tn].run() != 0:
                failed += 1
            else:
                passed += 1
        else:
            print("Error: No such test: \'" + tn + "\'")
            nonexist += 1

    print()
    print("Summary:")
    print("    Passed :", passed)
    print("    Failed :", failed)
    print("    Invalid:", nonexist)
    print("    Total  :", total)

if __name__ == "__main__":
    main()
