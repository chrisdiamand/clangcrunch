#!/usr/bin/env python

import os
import sys

# Load the compiler wrapper base class
if "LIBALLOCS_BASE" in os.environ:
    LIBALLOCS_BASE = os.environ["LIBALLOCS_BASE"]
else:
    LIBALLOCS_BASE = os.path.join(os.path.dirname(__file__), "../../../../liballocs")
LIBALLOCS_BASE = os.path.realpath(LIBALLOCS_BASE)

sys.path.append(os.path.join(LIBALLOCS_BASE, "tools"))
sys.path.append(os.path.join(LIBALLOCS_BASE, "tools/lang/c/lib"))
from allocscompilerwrapper import AllocsCompilerWrapper
from allocscc import AllocsCC

# HACK: we use this in allocscompilerwrapper's getCustomCompileArgs
os.environ["CC_IS_CLANG"] = "1"

class ClangAllocsCC(AllocsCC):

    def getClangArgs(self, sourceFiles):
        return ["-g", "-fno-eliminate-unused-debug-types"] \
            + self.getCustomCompileArgs(sourceFiles) \
            + (["-include", os.path.join(LIBALLOCS_BASE, \
                "include/liballocs_cil_inlines.h")] if (self.areAllSourceFilesC(sourceFiles) and \
                 len(sourceFiles) > 0) else [])

    def getUnderlyingCompilerCommand(self, sourceFiles):
        return ["clang", "-fsanitize=allocs"] + self.getClangArgs(sourceFiles)

if __name__ == '__main__':
    wrapper = ClangAllocsCC()
    ret = wrapper.main()
    exit(ret)
