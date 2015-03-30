#!/usr/bin/env python3

from os import path
import os
import subprocess
import sys

TESTDIR = path.realpath(path.dirname(__file__))

if "LIBALLOCS_BASE" in os.environ:
    LIBALLOCS_BASE = os.environ["LIBALLOCS_BASE"]
else:
    LIBALLOCS_BASE = path.join(TESTDIR, "../crunch/liballocs")
LIBALLOCS_BASE = path.realpath(LIBALLOCS_BASE)

if "LIBCRUNCH_BASE" in os.environ:
    LIBCRUNCH_BASE = os.environ["LIBCRUNCH_BASE"]
else:
    LIBCRUNCH_BASE = path.join(LIBALLOCS_BASE, "../libcrunch")
LIBCRUNCH_BASE = path.realpath(LIBCRUNCH_BASE)

CLEAN_EXTS = ["-allocsites.c", "-allocsites.so", "-types.c", "-types.c.log.gz",
              "-types.so", ".allocs", ".allocs.rej", ".allocstubs.c",
              ".allocstubs.i", ".allocstubs.o", ".cil.c", ".cil.i", ".cil.s",
              ".i", ".i.allocs", ".makelog", ".o", ".o.fixuplog", ".objallocs",
              ".s", ".srcallocs", ".srcallocs.rej"]

def runWithEnv(cmd, env = {}):
    assigns = ["%s='%s'" % (e, env[e]) for e in env]
    print(" ".join(assigns + cmd))
    wholeEnv = dict(os.environ)
    wholeEnv.update(env)
    proc = subprocess.Popen(cmd, env = wholeEnv)
    return proc.wait()

class Test:
    def run(self):
        self.clean()

        status = runWithEnv(self.getBuildCmd(), self.getBuildEnv())
        if status != 0:
            return status

        return runWithEnv(self.getRunCmd(), self.getRunEnv())

    def cleanFiles(self):
        return []

    def getBuildEnv(self):
        return {}

    def getRunEnv(self):
        return {}

    def clean(self):
        for f in self.getCleanFiles():
            if path.exists(f):
                os.unlink(f)

class AllocsTest(Test):
    def __init__(self, fname, buildEnv = {}, runEnv = {},
                 fail = False, flags = []):
        self.src_fname = fname
        self.out_fname = path.splitext(self.src_fname)[0]
        self.buildEnv = buildEnv
        self.runEnv = runEnv
        self.shouldFail = fail
        self.flags = flags

    def getCompiler(self):
        return "clang_allocscc"

    def getName(self):
        return self.out_fname

    def getBuildCmd(self):
        cmd = [self.getCompiler()]
        cmd += ["-std=c99", "-DUSE_STARTUP_BRK"]
        cmd += self.flags
        cmd += [self.src_fname, "-o", self.out_fname]
        return cmd

    def getBuildEnv(self):
        return self.buildEnv

    def getRunEnv(self):
        liballocs = path.join(LIBALLOCS_BASE, "lib/liballocs_preload.so")
        self.runEnv["LD_PRELOAD"] = path.realpath(liballocs)
        return self.runEnv

    def getRunCmd(self):
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

class StockAllocsTest(AllocsTest):
    def getBuildCmd(self):
        cmd = AllocsTest.getBuildCmd(self)
        # Without this argument there are "undefined reference to
        # `local_accessors'" errors.
        cmd = [cmd[0], "-gstrict-dwarf"] + cmd[1:]
        return cmd

    def getCompiler(self):
        return "allocscc"

    def getName(self):
        return "stock/" + AllocsTest.getName(self)

class CrunchTest(AllocsTest):
    def getCompiler(self):
        return "clang_crunchcc"

    def getBuildCmd(self):
        cmd = [self.getCompiler()]
        cmd += ["-D_GNU_SOURCE", "-std=c99", "-DUSE_STARTUP_BRK"]
        cmd += ["-I" + path.join(LIBCRUNCH_BASE, "include")]
        cmd += self.flags
        cmd += [self.src_fname, "-o", self.out_fname]
        return cmd

    def getRunEnv(self):
        liballocs = path.join(LIBCRUNCH_BASE, "lib/libcrunch_preload.so")
        self.runEnv["LD_PRELOAD"] = path.realpath(liballocs)
        return self.runEnv

class StockCrunchTest(CrunchTest):
    def getBuildCmd(self):
        cmd = CrunchTest.getBuildCmd(self)
        cmd = [cmd[0], "-gstrict-dwarf"] + cmd[1:]
        return cmd

    def getCompiler(self):
        return "crunchcc"

    def getName(self):
        return "stock/" + CrunchTest.getName(self)

def register_tests():
    tests = {}
    def add(t):
        assert isinstance(t, Test)
        name = t.getName()
        if name in tests:
            print("Error: Test '%s' already exists." % name)
        else:
            tests[t.getName()] = t

    def addAllocsTest(t):
        add(AllocsTest(t))
        add(StockAllocsTest(t))

    def addCrunchTest(t, buildEnv = {}, runEnv = {},
                      fail = False, flags = []):
        add(CrunchTest(t, buildEnv = buildEnv, runEnv = runEnv,
                       fail = fail, flags = flags))
        add(StockCrunchTest(t, buildEnv = buildEnv, runEnv = runEnv,
                            fail = fail, flags = flags))

    addAllocsTest("allocs/offsetof_composite.c")
    addAllocsTest("allocs/offsetof_simple.c")
    addAllocsTest("allocs/simple.c")

    addCrunchTest("crunch/array.c")
    addCrunchTest("crunch/fail_funptr.c", fail = True)
    addCrunchTest("crunch/function_refines.c")
    addCrunchTest("crunch/funptr.c",
                  buildEnv = {"LIBCRUNCH_SLOPPY_FUNCTION_POINTERS": "1"})
    addCrunchTest("crunch/heap.c")
    addCrunchTest("crunch/indirect.c", flags = ["-O0"])
    addCrunchTest("crunch/qualified_char.c")

    return tests

def zshcomp(tests, prefix = ""):
    tests = list(tests) + ["all", "clean"]
    tests.sort()
    for t in tests:
        print(prefix, t)

def helpAndExit(tests):
    print("Usage: %s TEST ..." % sys.argv[0])
    print("Available tests:")
    zshcomp(tests, prefix = "   ")
    sys.exit(0)

def main():
    tests = register_tests()

    if "zshcomp" in sys.argv:
        zshcomp(tests)
        sys.exit(0)

    if "clean" in sys.argv:
        for t in tests:
            tests[t].clean()
        for f in os.listdir(TESTDIR):
            for e in CLEAN_EXTS:
                fullpath = path.join(TESTDIR, f)
                if fullpath.endswith(e) and path.exists(fullpath):
                    os.unlink(fullpath)
        return 0

    testNames = sys.argv[1:]

    if len(testNames) == 0:
        helpAndExit(tests)

    if "all" in testNames:
        testNames = list(tests.keys())

    nonexist = 0
    passed = 0
    failed = 0
    failedTests = []
    total = len(testNames)

    for tn in testNames:
        if tn in tests:
            if tests[tn].run() != 0:
                failed += 1
                failedTests += [tn]
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

    if failed > 0:
        print("Failed tests:", " ".join(failedTests))

if __name__ == "__main__":
    main()
