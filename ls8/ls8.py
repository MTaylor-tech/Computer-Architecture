#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

cpu.load("examples/print8.ls8")
cpu.run()

cpu2 = CPU()
cpu2.load("examples/mult.ls8")
cpu2.run()
