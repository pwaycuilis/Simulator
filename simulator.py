import sys
from helpers import SetUp
import masking_constants as MASKs


class State():
    dataval = []
    PC = 96
    cycle = 1
    R = [0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, opcodes, dataval, addrs,
                 arg1, arg2, arg3, numInstructs,
                 opcodeStr, arg1Str, arg2Str,
                 arg3Str):
        # self.instructions = instrs
        self.opcode = opcodes
        self.dataval = dataval
        self.address = addrs
        self.numInstructions = numInstructs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.opcodeStr = opcodeStr
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str

    def getIndexOfMemAddress(self, currAddr):
        # ***
        num = (currAddr - 96) // 4
        return num
        # memIndex = 0
        # for i in self.address:
        #     if i == currAddr:
        #         return memIndex
        #     memIndex += 1
        # ****

    def incrementPC(self):
        self.PC = self.PC + 4

    def printState(self):

        outputFileName = SetUp.get_output_filename()

        with open(outputFileName + "_sim.txt", 'a') as outFile:

            i = self.getIndexOfMemAddress(self.PC)
            outFile.write("====================\n")
            outFile.write(
                "cycle:" + str(self.cycle) + "\t" + str(self.PC) + "\t" +
                self.opcodeStr[i] + self.arg1Str[i] + self.arg2Str[i] +
                self.arg3Str[i] + "\n")

            outFile.write("\n")
            outFile.write("registers:\n")
            outStr = "r00:"
            # ***
            # print(len(self.dataval))
            # iCount = 0
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])
                # REDACTED start
            outFile.write(outStr + "\n")

            outStr = "r08: "
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i + 8])

            outFile.write(outStr + "\n")

            outStr = "r16: "
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i + 16])

            outFile.write(outStr + "\n")

            outStr = "r24: "
            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i + 24])

            outFile.write(outStr + "\n")
            outFile.write("\ndata:\n")
            outStr = ""
            # REDACTED end

            for i in range(len(self.dataval)):
                # ****
                # print("Entering SECOND if loop")

                if (i % 8 == 0 and i != 0 or i == len(self.dataval)):
                    outFile.write(outStr + "\n")

                if i % 8 == 0:
                    outStr = str(self.address[i + self.numInstructions]) + \
                             ":" + str(self.dataval[i])

                    # print(outStr)

                if (i % 8 != 0):
                    outStr = outStr + "\t" + str(self.dataval[i])
            # print(outStr)
            outFile.write(outStr + "\n")
            outFile.close()


class Simulator():

    def __init__(self, opcode, dataval, address,
                 arg1, arg2, arg3, numInstructs,
                 opcodeStr, arg1Str, arg2Str,
                 arg3Str):
        self.opcode = opcode
        self.dataval = dataval
        self.address = address
        self.numInstructs = numInstructs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.opcodeStr = opcodeStr
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.specialMask = MASKs.specialMask

    def run(self):
        foundBreak = False
        armState = State(self.opcode, self.dataval,
                         self.address, self.arg1,
                         self.arg2, self.arg3,
                         self.numInstructs, self.opcodeStr,
                         self.arg1Str, self.arg2Str,
                         self.arg3Str)

        while (foundBreak == False):
            jumpAddr = armState.PC
            # get the next instruction
            i = armState.getIndexOfMemAddress(armState.PC)

            # TODO test and delete the need for instructions
            # if self.instructions[i] == '0000000000000000000000000000000':
            # NOP   this might still be wrong need to test more
            # print(self.opcode)
            # print(self.arg1)
            # print(self.arg2)
            # print(self.arg3)
            # print(i)
            # print(armState.R)
            # print(self.address)

            # print(self.dataval)

            # print(self.address[-1])

            # print(-9 >> 2)
            if (self.opcode[i] == 0):  # NOP
                armState.printState()
                armState.incrementPC()
                armState.cycle += 1
                continue  # go rightr back to top
            elif (self.opcode[i] >= 160 and self.opcode[i] <= 191):  # B
                # print(jumpAddr + ((self.arg1[i] * 4) - 4))
                jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)  # -4 takes care of increment pc later



            # CBZ
            elif (1440 <= self.opcode[i] <= 1447):
                if armState.R[self.arg1[i]] == 0:
                    jumpAddr = jumpAddr + ((self.arg2[i] * 4) - 4)

            # CBNZ
            elif 1448 <= self.opcode[i] <= 1455:
                if armState.R[self.arg1[i]] != 0:
                    jumpAddr = jumpAddr + ((self.arg2[i] * 4) - 4)

            # AND
            elif self.opcode[i] == 1104:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] & armState.R[self.arg2[i]]

            # ORR
            elif self.opcode[i] == 1360:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] | armState.R[self.arg2[i]]

            # EOR
            elif self.opcode[i] == 1872:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] ^ armState.R[self.arg2[i]]


            # ADDI
            elif (1160 <= self.opcode[i] <= 1161):
                # R[i] =
                armState.R[self.arg1[i]] = armState.R[self.arg2[i]] + self.arg3[i]

            # SUBI
            elif (1672 <= self.opcode[i] <= 1673):
                armState.R[self.arg1[i]] = armState.R[self.arg2[i]] - self.arg3[i]

            # ADD (args 1-3 in diff order)
            elif self.opcode[i] == 1112:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] + armState.R[self.arg2[i]]


            # SUB (args 1-3 in diff order) arg3 = arg1 - arg2
            elif self.opcode[i] == 1624:
                armState.R[self.arg3[i]] = armState.R[self.arg1[i]] - armState.R[self.arg2[i]]


            # MOVZ

            # MOVZ
            elif 1684 <= self.opcode[i] <= 1687:
                armState.R[self.arg1[i]] = self.arg2[i] * (2 ** (self.arg3[i]))
                # print("MOVZ")

            # MOVK
            elif 1940 <= self.opcode[i] <= 1943:
                if self.arg3[i] == 0:
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] & 0xFFFFFFFFFFFF0000
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] + self.arg2[i]

                elif self.arg3[i] == 16:
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] & 0xFFFFFFFF0000FFFF
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] + (self.arg2[i] * (2 ** 16))

                elif self.arg3[i] == 32:
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] & 0xFFFF0000FFFFFFFF
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] + (self.arg2[i] * (2 ** 32))

                elif self.arg3[i] == 48:
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] & 0x0000FFFFFFFFFFFF
                    armState.R[self.arg1[i]] = armState.R[self.arg1[i]] + (self.arg2[i] * (2 ** 48))

            # ASR
            elif self.opcode[i] == 1692:
                # armState.R[self.arg2[i]] = armState.R[self.arg1[i]] >> 1
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] >> self.arg1[i]

            # LSR R0, R1, #4  Type R
            elif self.opcode[i] == 1690:
                # print(self.arg3[])

                # print(~armState.R[self.arg2[i]])
                if armState.R[self.arg2[i]] >= 0:
                    # print(">= 0")
                    armState.R[self.arg3[i]] = armState.R[self.arg2[i]] >> self.arg1[i]
                else:
                    # #print("else (<0) ")
                    # msb = 1
                    # #exp = 0
                    # #2s comp neg number padded with 0 instead = pos num + the amount of from most sig bit
                    # #example: -112 = -128 + 16  , padded with zeros the number would be 128 + 16 = 144
                    # #so after finding the -128 ,  convert it to 144 then bitshift to right
                    #
                    # while (-msb > armState.R[self.arg2[i]]):
                    #     msb = msb * 2   #find value of most significant bit
                    #     #exp += 1    #find most significant bit
                    #     #print(exp)
                    #     #print(msb)
                    #
                    # newNum = msb - (armState.R[self.arg2[i]] * (-1))
                    # #print(newNum)
                    # #armState.R[self.arg3[i]] = msb + newNum
                    # msb += newNum
                    # armState.R[self.arg3[i]] = msb >> self.arg1[i]

                    armState.R[self.arg3[i]] = (armState.R[self.arg2[i]] % (1 << 32) >> self.arg1[i])

                    # armState.R[self.arg3[i]] = (armState.R[self.arg2[i]] + 0x80000000) >> self.arg1[i]

                # armState.R[self.arg3[i]] = (armState.R[self.arg2[i]] % 0x100000000) >> self.arg1[i]

            # LSL R0, R1, #4  Type R
            elif self.opcode[i] == 1691:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] << self.arg1[i]

            # STUR
            elif self.opcode[i] == 1984:
                # print("Entering store instruction")
                if (armState.R[self.arg2[i]] + (self.arg3[i]) * 4) > self.address[-1]:

                    numAppend = ((armState.R[self.arg2[i]] + self.arg3[i] * 4) - self.address[-1]) // 4
                    # print(armState.R[self.arg2[i]] + (self.arg3[i]*4))
                    # print(self.address[-1])
                    # print(numAppend)

                    for z in range(numAppend):
                        self.address.append(self.address[-1] + 4)
                        self.dataval.append(0)

                    self.dataval[-1] = armState.R[self.arg1[i]]

                    while (len(self.dataval) % 8 != 0):
                        self.address.append(self.address[-1] + 4)
                        self.dataval.append(0)





                elif (armState.R[self.arg2[i]] + self.arg3[i] * 4) <= self.address[-1]:
                    for n in range(len(self.address)):
                        if armState.R[self.arg2[i]] + (self.arg3[i] * 4) == self.address[n]:
                            self.dataval[n - self.numInstructs] = armState.R[self.arg1[i]]

                # if (armState.R[self.arg2[i]] + (self.arg3[i]) * 4) > self.address[-1]:
                #     storeIndex = armState.getIndexOfMemAddress(armState.R[self.arg2[i]] + (self.arg3[i]*4))
                #     lastIndex = armState.getIndexOfMemAddress(self.address[-1])
                #     print(armState.R[self.arg2[i]] + (self.arg3[i]*4))
                #     print(self.address[-1])
                #     print(storeIndex)
                #     print(lastIndex)
                #     print(storeIndex - lastIndex)
                #     for z in range(storeIndex-lastIndex):
                #         self.address.append(self.address[-1] + 4 )
                #         self.dataval.append(0)
                #
                #     self.dataval.append(armState.R[self.arg1[i]])











            # LDUR R1, [R2, #100]

            # LDUR
            elif self.opcode[i] == 1986:
                for n in range(len(self.address)):
                    if armState.R[self.arg2[i]] + (self.arg3[i] * 4) == self.address[n]:
                        # print("inlist")
                        armState.R[self.arg1[i]] = self.dataval[n - self.numInstructs]
                        # self.dataval[n - self.numInstructs] = armState.R[self.arg1[i]]

                # armState.R[self.arg1[i]] = self.dataval[

                # if no address exists, append it

            # TODO test and delete the need for instructions

            elif self.opcode[i] == 2038:
                # and (int(self.instruictions[i], base=2) & self.specialMask) == 20319591 #BREAK
                foundBreak = True

            else:
                print("IN SIM -- UNKNOWN INSTRUCTION --------------------- !!!")

            armState.printState()
            armState.PC = jumpAddr
            armState.incrementPC()
            armState.cycle += 1






