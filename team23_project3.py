#!/usr/bin/python3


import disassembler
import writeBack
import simulator

import simClass

mydis = disassembler.Disassembler()
output = {}
output = mydis.run()

mydis.print()

sim = simClass.simClass(**output)
sim.run()







# import d  isassembler
# import simulator
#
# mydis = disassembler.Disassembler()
# output = {}
# output = mydis.run()
#
# mydis.print()
#
#
#
# mysim = simulator.Simulator(**output)
# mysim.run()



#output.instructions,
#mysim = simulator.Simulator(output.instructions, output.opcode, output.dataval,
#                          output.address, output.arg1, output.arg2, output.arg3,
#                          output.numInstructs, output.opcodeStr, output.arg1Str,
#                          output.arg2Str, output.arg3Str)
