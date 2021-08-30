import writeBack
import alu
import cache
import issue
import fetch
import simulator
import memory
from helpers import SetUp

gobal_cycle = 0
class simClass:
    #instruction

    # R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #
    # postMemBuff = [-1, -1]
    # postALUBuff = [-1, -1]
    # preMemBuff = [-1, -1]
    # preALUBuff = [-1, -1]
    # preIssueBuff = [-1, -1, -1, -1]
    def __init__(self, instructions, opcode, opcodeStr, dataval,
                address, arg1, arg2, arg3, arg1Str, arg2Str, arg3Str,
                numInstructs, destReg, src1Reg, src2Reg ):
        self.instruction = instructions
        self.opcode = opcode
        self.dataval = dataval
        self.address = address
        self.numInstructions = numInstructs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.arg1Str = arg1Str
        self.arg2Str = arg2Str
        self.arg3Str = arg3Str
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.opcodeStr = opcodeStr
        self.PC = 96
        self.cycle = 1
        self.cycleList = [0]
        self.R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.postMemBuff = [-1, -1] #first num is value, second is instr index
        self.postALUBuff = [-1, -1]  #first num is value, second is instr index
        self.preMemBuff = [-1, -1]
        self.preALUBuff = [-1, -1]
        self.preIssueBuff = [-1, -1, -1, -1]



        #TESTING end



        # self.preIssueBuff = [0, 1, 2, 3]


        self.WB = writeBack.WriteBack(self.R, self.postMemBuff, self.postALUBuff, destReg)
        #self.WB = WriteBack(self.R, self.postMemBuff, self.postALUBuff, destReg)

        self.cache = cache.Cache(numInstructs, instructions, dataval, address)
        self.ALU = alu.ALU(self.R, self.postALUBuff, self.preALUBuff, opcodeStr, arg1, arg2, arg3)
        #self.cache = cache.Cache(numInstructs, instructions, dataval, address)
        #order important? had cache after alu but slide has this order (cache then alu)

        self.MEM = memory.Memory(self.R, self.postMemBuff, self.preMemBuff, opcodeStr, arg1, arg2,
                                 arg3, dataval, address, self.numInstructions, self.cache, self.cycleList)

        self.issue = issue.Issue(self.preIssueBuff, self.preMemBuff, self.preALUBuff,
                                 instructions, opcode, opcodeStr, dataval, address, arg1, arg2, arg3,
                                numInstructs, destReg, src1Reg, src2Reg)

        self.fetch = fetch.Fetch(self.preIssueBuff, instructions, opcode, opcodeStr, dataval, address, arg1, arg2, arg3,
                                 numInstructs, destReg, src1Reg, src2Reg)

        self.outputFileName = SetUp.get_output_filename()

        #print(self.cache)
    def run(self):
        go = True

        while go:

            # self.WB.run()
            # self.ALU.run()
            # #self.MEM.run()
            # self.issue.run()
            # #go = self.fetch.run()
            #
            # self.printState()
            # self.cycle += 1
            # print(f"cycle:{self.cycle}")
            #for testing purposes

            # self.issue.preIssueBuff = [0, 1, 2, 3]

            #update buffers from WB
            # [self.R, self.postMemBuff, self.postALUBuff] = self.WB.run()
            print(f"(simClass102)opcodestr : {self.opcodeStr}")
            print(f"(simClass103)self.preIssueBuff : {self.preIssueBuff}")
            print(f"(simClass104)self.arg1Str : {self.arg1Str}")

            #self.WB.run()
            [self.R, self.postMemBuff, self.postALUBuff, self.destReg] = self.WB.run()
            #update Buffers from ALU
            print(f"(SimClass109)self.postMemBuff = {self.postMemBuff}")
            [self.preALUBuff, self.postALUBuff] = self.ALU.run()
            [self.preMemBuff, self.postMemBuff] = self.MEM.run()
            [self.preMemBuff, self.preALUBuff, self.preIssueBuff] = self.issue.run()
            self.preIssueBuff = self.fetch.run()
            print(f"simClass(113)self.postMemBuff = {self.postMemBuff}")
            # send new buffers values to WB
            #uncommented originally and line 106
            self.WB = writeBack.WriteBack(self.R, self.postMemBuff, self.postALUBuff, self.destReg)

            self.printState()
            self.cycle += 1



            if self.cycle > 22:
                go = False


    def printState(self):
        #print(f"simClass self.R: {self.R}")



        #print(f"postALUBuff from printstate:{self.postALUBuff}")

        print(f"Cycle:{self.cycle}")
        #
        print("Pre-Issue Buffer:")
        print(f"\tEntry 0:\t{self.opcodeStr[self.preIssueBuff[0]]}"
              f"{self.arg1Str[self.preIssueBuff[0]]}{self.arg2Str[self.preIssueBuff[0]]}"
              f"{self.arg3Str[self.preIssueBuff[0]]}")

        #outFile.write("\tEntry 0:\t" + self.opcodeStr[self.preIssueBuff[0]] + self.arg1Str[self.preIssueBuff[0]] +
        #              self.arg2Str[self.preIssueBuff[0]] + self.arg3Str[self.preIssueBuff[0]] + "\n")
        #
        print(f"\tEntry 1:\t{self.opcodeStr[self.preIssueBuff[1]]}"
              f"{self.arg1Str[self.preIssueBuff[1]]}{self.arg2Str[self.preIssueBuff[1]]}"
              f"{self.arg3Str[self.preIssueBuff[1]]}")
        #
        print(f"\tEntry 2:\t{self.opcodeStr[self.preIssueBuff[2]]}"
              f"{self.arg1Str[self.preIssueBuff[2]]}{self.arg2Str[self.preIssueBuff[2]]}"
              f"{self.arg3Str[self.preIssueBuff[2]]}")
        #
        print(f"\tEntry 3:\t{self.opcodeStr[self.preIssueBuff[3]]}"
              f"{self.arg1Str[self.preIssueBuff[3]]}{self.arg2Str[self.preIssueBuff[3]]}"
              f"{self.arg3Str[self.preIssueBuff[3]]}")
        #
        #going into ALU
        print("Pre_ALU Queue:")
        print(f"\tEntry 0:\t{self.opcodeStr[self.preALUBuff[0]]}"
              f"{self.arg1Str[self.preALUBuff[0]]}{self.arg2Str[self.preALUBuff[0]]}"
              f"{self.arg3Str[self.preALUBuff[0]]}")
        #
        #going into ALU
        print(f"\tEntry 1:\t{self.opcodeStr[self.preALUBuff[1]]}"
              f"{self.arg1Str[self.preALUBuff[1]]}{self.arg2Str[self.preALUBuff[1]]}"
              f"{self.arg3Str[self.preALUBuff[1]]}")
        #
        # #going into WB                   self.postALUBuff shouldx be [0] or [1] ??
        print("Post_ALU Queue:")
        print(f"\tEntry 0:\t{self.opcodeStr[self.postALUBuff[1]]}"
              f"{self.arg1Str[self.postALUBuff[1]]}{self.arg2Str[self.postALUBuff[1]]}"
              f"{self.arg3Str[self.postALUBuff[1]]}")
        #
        # # print(f"\tEntry 1:\t{self.opcodeStr[self.preALUBuff[1]]}"
        # #       f"{self.arg1Str[self.preALUBuff[1]]}{self.arg2Str[self.preALUBuff[1]]}"
        # #       f"{self.arg3Str[self.preALUBuff[1]]}")

        #NEED TO ADD TO outWrite section also
        print("Pre_MEM Queue:")
        print(f"\tEntry 0:\t{self.opcodeStr[self.preMemBuff[0]]}"
              f"{self.arg1Str[self.preMemBuff[0]]}{self.arg2Str[self.preMemBuff[0]]}"
              f"{self.arg3Str[self.preMemBuff[0]]}")

        print(f"\tEntry 1:\t{self.opcodeStr[self.preMemBuff[1]]}"
              f"{self.arg1Str[self.preMemBuff[1]]}{self.arg2Str[self.preMemBuff[1]]}"
              f"{self.arg3Str[self.preMemBuff[1]]}")
        #
        #print(f"(simClass187)self.postMemBuff = {self.postMemBuff}")
        #
        print("Post_MEM Queue:")    #index number in postMemBuff[1]
        print(f"\tEntry 0:\t{self.opcodeStr[self.postMemBuff[1]]}"
              f"{self.arg1Str[self.postMemBuff[1]]}{self.arg2Str[self.postMemBuff[1]]}"
              f"{self.arg3Str[self.postMemBuff[1]]}")

        print(f"self.R{self.R}")
        #
        LRU = 0
        #
        #
        #
        # # return [True, self.cacheSets[setNum][(self.lruBit[setNum] + 1) % 2][dataWord + 3]]
        #
        #
        print("Cache")
        print(f"Set 0: LRU = {self.cache.lruBit[0]}")
        print(f"\tEntry 0:{self.fetch.cache.cacheSets[0][0]}")
        #print(f"\tEntry 0:{self.fetch.cache.}")
        print(f"\tEntry 1:{self.fetch.cache.cacheSets[0][1]}")


        print(f"Set 1: LRU = {self.cache.lruBit[1]}")
        print(f"\tEntry 0:{self.fetch.cache.cacheSets[1][0]}")
        print(f"\tEntry 1:{self.fetch.cache.cacheSets[1][1]}")


        print(f"Set 2: LRU = {self.cache.lruBit[2]}")
        print(f"\tEntry 0:{self.fetch.cache.cacheSets[2][0]}")
        print(f"\tEntry 1:{self.fetch.cache.cacheSets[2][1]}")

        print(f"Set 3: LRU = {self.cache.lruBit[3]}")
        print(f"\tEntry 0:{self.fetch.cache.cacheSets[3][0]}")
        print(f"\tEntry 1:{self.fetch.cache.cacheSets[3][1]}")

        # print(f"\tEntry 0:[({self.fetch.cache.cacheSets[0]},{self.fetch.cache.cacheSets[1]},"
        #       f"{self.fetch.cache.cacheSets[2]})<{self.fetch.cache.cacheSets[3]},"
        #       f"{self.fetch.cache.cacheSets[0]}>]")
        #outFile.write("Cache\n")
        #outFile.write("Set 0: LRU = " + self.cache.lruBit[0])
        #outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[0][0]))
        #outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[0][1]))

        #outFile.write("\nSet 1: LRU = " + self.cache.lruBit[1])
        #outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[1][0]))
        #outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[1][1]))

        #outFile.write("\nSet 2: LRU = " + self.cache.lruBit[2])
        #outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[2][0]))
        #outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[2][1]))

        #outFile.write("\nSet 3: LRU = " + self.cache.lruBit[3])
        #outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[3][0]))
        #outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[3][1]))
        print(f"\ndata:\n")
        for i in range(len(self.dataval)):
            if (i % 8 == 0 and i!= 0) or i == len(self.dataval):
                print(f" ")

            if i % 8 == 0:
                print(f"{self.address[i + self.numInstructions]} : {self.dataval[i]}", end = "")

            if i % 8 != 0:
                print(f"\t {self.dataval[i]}", end ="" )

        print(f"")

        """
        outFile.write("\ndata:\n")
        outStr = ""
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
       """




        #testing
        #print(f"{range(len(self.instruction))}")

        outputFileName = SetUp.get_output_filename()

        with open(outputFileName + "_pipeline.txt", 'a') as outFile:

            breakChanger = []


            #ALSO LINE ~378 for undo of this
            for i in range(len(self.instruction)):
                if self.opcodeStr[i] == "BREAK":
                    self.opcodeStr[i] = ""


            outFile.write("---------------------\n")
            outFile.write(
                "cycle:" + str(self.cycle) + "\t" + "\n")

            outFile.write("Pre-Issue Buffer:\n")
            outFile.write("\tEntry 0:\t" + self.opcodeStr[self.preIssueBuff[0]] + self.arg1Str[self.preIssueBuff[0]] +
                          self.arg2Str[self.preIssueBuff[0]] + self.arg3Str[self.preIssueBuff[0]] + "\n")

            outFile.write("\tEntry 1:\t" + self.opcodeStr[self.preIssueBuff[1]] + self.arg1Str[self.preIssueBuff[1]] +
                          self.arg2Str[self.preIssueBuff[1]]+ self.arg3Str[self.preIssueBuff[1]] + "\n")

            outFile.write("\tEntry 2:\t" + self.opcodeStr[self.preIssueBuff[2]] + self.arg1Str[self.preIssueBuff[2]] +
                          self.arg2Str[self.preIssueBuff[2]] + self.arg3Str[self.preIssueBuff[2]] + "\n")

            outFile.write("\tEntry 3:\t" + self.opcodeStr[self.preIssueBuff[3]] + self.arg1Str[self.preIssueBuff[3]] +
                          self.arg2Str[self.preIssueBuff[3]] + self.arg3Str[self.preIssueBuff[3]] + "\n")

            outFile.write("Pre_ALU Queue:\n")
            outFile.write("\tEntry 0:\t" + self.opcodeStr[self.preALUBuff[0]] + self.arg1Str[self.preALUBuff[0]] +
                          self.arg2Str[self.preALUBuff[0]] + self.arg3Str[self.preALUBuff[0]] + "\n")

            outFile.write("\tEntry 1:\t" + self.opcodeStr[self.preALUBuff[1]] + self.arg1Str[self.preALUBuff[1]] +
                          self.arg2Str[self.preALUBuff[1]] + self.arg3Str[self.preALUBuff[1]] + "\n")


            outFile.write("Post_ALU Queue:\n")
            outFile.write("\tEntry 0:\t" + self.opcodeStr[self.postALUBuff[1]] + self.arg1Str[self.postALUBuff[1]] +
                          self.arg2Str[self.postALUBuff[1]] + self.arg3Str[self.postALUBuff[1]] + "\n")

            #outFile.write("\n")

            outFile.write("Pre_MEM Queue:\n")
            outFile.write("\tEntry 0:\t" + self.opcodeStr[self.preMemBuff[0]] + self.arg1Str[self.preMemBuff[0]] +
                          self.arg2Str[self.preMemBuff[0]] + self.arg3Str[self.preMemBuff[0]] + "\n")
            outFile.write("\tEntry 1:\t" + self.opcodeStr[self.preMemBuff[1]] + self.arg1Str[self.preMemBuff[1]] +
                          self.arg2Str[self.preMemBuff[1]] + self.arg3Str[self.preMemBuff[1]] + "\n")

            outFile.write("Post_MEM Queue:\n")  #index in postMemBuff[0]
            outFile.write("\tEntry 0:\t" + self.opcodeStr[self.postMemBuff[1]] + self.arg1Str[self.postMemBuff[1]] +
                          self.arg2Str[self.postMemBuff[1]] + self.arg3Str[self.postMemBuff[1]] + "\n")
            # NEED TO ADD TO outWrite section also
            #print("Pre_MEM Queue:")
            #print(f"\tEntry 0:\t{self.opcodeStr[self.preMemBuff[0]]}"
            #      f"{self.arg1Str[self.preMemBuff[0]]}{self.arg2Str[self.preMemBuff[0]]}"
            #      f"{self.arg3Str[self.preMemBuff[0]]}")

            #print(f"\tEntry 1:\t{self.opcodeStr[self.preMemBuff[1]]}"
            #      f"{self.arg1Str[self.preMemBuff[1]]}{self.arg2Str[self.preMemBuff[1]]}"
            #      f"{self.arg3Str[self.preMemBuff[1]]}")

            #print("Post_MEM Queue:")
            #print(f"\tEntry 0:\t{self.opcodeStr[self.postMemBuff[0]]}"
            #      f"{self.arg1Str[self.postMemBuff[0]]}{self.arg2Str[self.postMemBuff[0]]}"
            #      f"{self.arg3Str[self.postMemBuff[0]]}")
            outFile.write("registers:\n")
            outStr = "r00:"

            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])

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

            outFile.write("Cache\n")
            outFile.write("Set 0: LRU = " + str(self.cache.lruBit[0]))
            outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[0][0]))
            outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[0][1]))

            outFile.write("\nSet 1: LRU = " + str(self.cache.lruBit[1]))
            outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[1][0]))
            outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[1][1]))

            outFile.write("\nSet 2: LRU = " + str(self.cache.lruBit[2]))
            outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[2][0]))
            outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[2][1]))

            outFile.write("\nSet 3: LRU = " + str(self.cache.lruBit[3]))
            outFile.write("\n\tEntry 0:" + str(self.fetch.cache.cacheSets[3][0]))
            outFile.write("\n\tEntry 1:" + str(self.fetch.cache.cacheSets[3][1]))


            # print("Cache")
            # print(f"Set 0: LRU = {LRU}")
            # print(f"\tEntry 0:{self.fetch.cache.cacheSets[0][0]}")
            # print(f"\tEntry 1:{self.fetch.cache.cacheSets[0][1]}")


            outFile.write("\ndata:\n")
            outStr = ""
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
            #ALSO line ~265 first part of this
            for i in range(len(self.instruction)):
                if self.opcodeStr[i] == "":
                    self.opcodeStr[i] = "BREAK"












        #print(f"\tEntry 1:\t{self.opcodeStr[self.preALUBuff[1]]}")

        # print(f"self.WB.R{self.WB.R}")
        # print(f"self.R{self.R}")
        # print(f"self.ALU.preALUBuff{self.ALU.preALUBuff}")
        # print(f"self.preALUBuff{self.preALUBuff}")
        #
        # print(f"self.ALU.postALUBuff{self.ALU.postALUBuff}")
        # print(f"self.postALUBuff{self.postALUBuff}")


    # def printState(self):
    #
    #     outputFileName = SetUp.get_output_filename()
    #
    #     with open(outputFileName + "_pipeline.txt", 'a') as outFile:
    #
    #         i = self.getIndexOfMemAddress(self.PC)
    #         outFile.write("---------------------\n")
    #         outFile.write(
    #             "cycle:" + str(self.cycle) + "\t" + "\n")
    #
    #         outFile.write("Pre-Issue Buffer:\n")
    #         outFile.write("\tEntry 0:\t" + self.arg1Str[self.preIssueBuff[0]] + self.arg2Str[self.preIssueBuff[0]]
    #                       + self.arg3Str[self.preIssueBuff[0]])

            # print(f"\tEntry 0:\t{self.opcodeStr[self.preIssueBuff[0]]}"
            #       f"{self.arg1Str[self.preIssueBuff[0]]}{self.arg2Str[self.preIssueBuff[0]]}"
            #       f"{self.arg3Str[self.preIssueBuff[0]]}")

            # outFile.write("\n")
            # outFile.write("registers:\n")
            # outStr = "r00:"
            # # ***
            # # print(len(self.dataval))
            # # iCount = 0
            # for i in range(0, 8):
            #     outStr = outStr + "\t" + str(self.R[i])
            #     # REDACTED start
            # outFile.write(outStr + "\n")
            #
            # outStr = "r08: "
            # for i in range(0, 8):
            #     outStr = outStr + "\t" + str(self.R[i + 8])
            #
            # outFile.write(outStr + "\n")
            #
            # outStr = "r16: "
            # for i in range(0, 8):
            #     outStr = outStr + "\t" + str(self.R[i + 16])
            #
            # outFile.write(outStr + "\n")
            #
            # outStr = "r24: "
            # for i in range(0, 8):
            #     outStr = outStr + "\t" + str(self.R[i + 24])
            #
            # outFile.write(outStr + "\n")
            # outFile.write("\ndata:\n")
            # outStr = ""
            # # REDACTED end
            #
            # for i in range(len(self.dataval)):
            #     # ****
            #     # print("Entering SECOND if loop")
            #
            #     if (i % 8 == 0 and i != 0 or i == len(self.dataval)):
            #         outFile.write(outStr + "\n")
            #
            #     if i % 8 == 0:
            #         outStr = str(self.address[i + self.numInstructions]) + \
            #                  ":" + str(self.dataval[i])
            #
            #         # print(outStr)
            #
            #     if (i % 8 != 0):
            #         outStr = outStr + "\t" + str(self.dataval[i])
            # # print(outStr)
            # outFile.write(outStr + "\n")
            # outFile.close()

