#!/usr/bin/env python

import os
import sys

# Load the compiler wrapper base class
if "LIBALLOCS_BASE" in os.environ:
    LIBALLOCS_BASE = os.environ["LIBALLOCS_BASE"]
else:
    LIBALLOCS_BASE = os.path.join(os.path.dirname(__file__), "../crunch/liballocs")
LIBALLOCS_BASE = os.path.realpath(LIBALLOCS_BASE)

sys.path.append(os.path.join(LIBALLOCS_BASE, "tools"))
from allocscompilerwrapper import AllocsCompilerWrapper

class ClangAllocsCC(AllocsCompilerWrapper):

    def defaultL1AllocFns(self):
        return ["malloc(Z)p", "calloc(zZ)p", "realloc(pZ)p", "memalign(zZ)p"]

    def defaultFreeFns(self):
        return ["free(P)"]

    def makeObjectFileName(self, sourceFile):
            nameStem, nameExtension = os.path.splitext(sourceFile)
            if (nameExtension == ".c"):
                outputFilename = nameStem + ".o"
                self.debugMsg("Making a secret output file (from .c source) " +
                              outputFilename + "\n")
            else:
                outputFilename = sourceFile + ".o"
                self.debugMsg("Making a secret output file (from unknown source) " +
                              outputFilename + "\n")
            return outputFilename

    def getCustomCompileArgs(self, sourceInputFiles):
        return ["-gdwarf-4", "-fno-omit-frame-pointer", "-ffunction-sections"]

    def getClangArgs(self, sourceFiles):
        # Only use -include for C files.
        allSourceFilesAreC = True
        for sourceFile in sourceFiles:
            if sourceFile.lang != "c" and not sourceFile.endswith(".c"):
                allSourceFilesAreC = False

        includeArgs = []
        # We can only do monalloca, and anything else that involves -include,
        # if we're compiling only C files.
        if len(sourceFiles) > 0 and allSourceFilesAreC:
            self.debugMsg("All source files (%d) are C files\n" % len(sourceFiles))
            cil_inlines = os.path.join(LIBALLOCS_BASE,
                                       "include/liballocs_cil_inlines.h")
            includeArgs = ["-include", cil_inlines]
        else:
            self.debugMsg("No source files, or not all (only %d) are C files\n" % len(sourceFiles))

        ret = ["-g", "-fno-eliminate-unused-debug-types"]
        return ret + includeArgs

    def getUnderlyingCompilerCommand(self, sourceFiles):
        return ["clang", "-fsanitize=allocs"] + self.getClangArgs(sourceFiles)

    def runUnderlyingCompiler(self, sourceFiles, options):
        ret1 = AllocsCompilerWrapper.runUnderlyingCompiler(self, sourceFiles, options)
        if (ret1 != 0):
            self.debugMsg("Underlying compiler exited with status %d." % ret1)
            cmd = self.getUnderlyingCompilerCommand(sourceFiles) + options
            self.debugMsg("Command was: " + " ".join(cmd))
            sys.exit(-1)
        return ret1

if __name__ == '__main__':
    wrapper = ClangAllocsCC()
    ret = wrapper.main()
    exit(ret)
