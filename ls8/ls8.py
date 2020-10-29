#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

flag = sys.argv[1]
if len(flag) > 2:
    cpu.load(flag)
else:
    if flag=="-f":
        cpu.load(sys.argv[2])
    else:
        cpu.load(f"examples/{sys.argv[2]}.ls8")
# cpu.load("examples/stack.ls8")
cpu.run()

# cpu.load("examples/stack.ls8")
# cpu.run()
