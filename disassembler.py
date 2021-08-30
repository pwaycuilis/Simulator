from helpers import SetUp
import os
import masking_constants as MASKs
import sys

###uncommented instructions

class Disassembler:
    opcodeStr = []
    instrSpaced = []
    arg1 = []
    arg2 = []
    arg3 = []
    arg1Str = []
    arg2Str = []
    arg3Str = []
    dataval = []
    rawdata = []
    address = []
    destReg = []
    src1Reg = []
    src2Reg = []
    numInstructs = 0

    def run(self):

        instructions = []

        instructions = SetUp.get_input_filename()

        instructions = SetUp.import_data_file()

        outputFilename = SetUp.get_output_filename()

        print("raw output filename is ", outputFilename)

        for i in range(len(instructions)):
            self.address.append(96 + (i * 4))

        opcode = []

        for z in instructions:
            opcode.append(int(z, base=2) >> 21)

        for i in range(len(opcode)):
            self.numInstructs = self.numInstructs + 1
            if opcode[i] == 1112:
                # ADD

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ADD")

                # ADD R3, R1, R2
                # R1

                self.arg1.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)

                # R2

                self.arg2.append((int(instructions[i], base=2) & MASKs.rmMask) >> 16)
                # R3

                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])

                # SUB R3, R1, R2
            elif opcode[i] == 1624:

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("SUB")

                # arg3 = arg1 - arg2
                self.arg1.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                # arg1Str = arg2Str - arg3Str
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

                self.destReg.append(self.arg3[i])   #rd (SUB Rd = Rn - Rm)
                self.src1Reg.append(self.arg1[i])   #rn
                self.src2Reg.append(self.arg2[i])   #rm

                # AND
            elif opcode[i] == 1104:

                # *****
                # print(instructions[i])
                # *****
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("AND")

                self.arg1.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])

            # ORR
            elif opcode[i] == 1360:

                # *****
                # print(instructions[i])

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ORR")

                self.arg1.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)

                self.arg2.append((int(instructions[i], base=2) & MASKs.rmMask) >> 16)

                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(self.arg2[i])

                # B   range 160-191
            elif 160 <= opcode[i] <= 191:

                self.instrSpaced.append(SetUp.bin2StringSpacedB(instructions[i]))
                self.opcodeStr.append("B")

                self.arg1.append(SetUp.imm_bit_to_32_bit_converter((int(instructions[i], base=2) & MASKs.bMask), 26))
                self.arg2.append(0)
                self.arg3.append(0)

                self.arg1Str.append("\t#" + str(self.arg1[i]))
                self.arg2Str.append("")
                self.arg3Str.append("")

                self.destReg.append(-18)
                self.src1Reg.append(-17)
                self.src2Reg.append(-16)

                # ADDI
            elif 1160 <= opcode[i] <= 1161:

                self.instrSpaced.append(SetUp.bin2StringSpacedI(instructions[i]))
                self.opcodeStr.append("ADDI")

                # R1
                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)
                # R2
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.imMask) >> 10)

                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]))

                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(-10)

                # SUBI
            elif 1672 <= opcode[i] <= 1673:

                self.instrSpaced.append(SetUp.bin2StringSpacedI(instructions[i]))
                self.opcodeStr.append("SUBI")

                # R1
                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)
                # R2
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.imMask) >> 10)

                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]))

                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(-11)

                # LDUR
            elif opcode[i] == 1986:

                # type D??
                self.instrSpaced.append(SetUp.bin2StringSpacedD(instructions[i]))
                self.opcodeStr.append("LDUR")

                # R1

                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.addrMask) >> 12)

                # LDUR R1, [R2, #100]
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", [R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]) + "]")

                #LDUR RD = [RN + offset]
                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg3[i])

                # STUR
            elif opcode[i] == 1984:

                # type D??
                self.instrSpaced.append(SetUp.bin2StringSpacedD(instructions[i]))
                self.opcodeStr.append("STUR")

                # R1

                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.addrMask) >> 12)

                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", [R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg3[i]) + "]")

                self.destReg.append(self.arg1[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg3[i])


            # CBZ
            elif 1440 <= opcode[i] <= 1447:

                # type D??
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(instructions[i]))
                self.opcodeStr.append("CBZ")

                # R19

                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)
                self.arg2.append(
                    SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & MASKs.addr2Mask) >> 5), 19))
                self.arg3.append(0)

                # CBZ R19, #-3
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", #" + str(self.arg2[i]))
                self.arg3Str.append("")

                self.destReg.append(-12)
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(-13)

            # CBNZ
            elif 1448 <= opcode[i] <= 1455:

                # type D??
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(instructions[i]))
                self.opcodeStr.append("CBNZ")

                # R19

                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg2.append(
                    SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & MASKs.addr2Mask) >> 5), 19))
                self.arg3.append(0)

                # CBZ R19, #-3
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", #" + str(self.arg2[i]))
                self.arg3Str.append("")

                self.destReg.append(-14)
                self.src1Reg.append(self.arg1[i])
                self.src2Reg.append(-15)

                # MOVZ R1, 255, LSL 0
            elif 1684 <= opcode[i] <= 1687:

                # *****
                # print(instructions[i])

                # type D??
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(instructions[i]))
                self.opcodeStr.append("MOVZ")

                # R1
                # self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg2.append((int(instructions[i], base=2) & MASKs.imdataMask) >> 5)
                # bitshift 17 because its result * 16
                self.arg3.append((int(instructions[i], base=2) & MASKs.imsftMask) >> 17)

                # MOVZ R1, 255, LSL 0
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", " + str(self.arg2[i]))
                self.arg3Str.append(", LSL " + str(self.arg3[i]))

                # MOVK R2, 65280, LSL 48
            elif 1940 <= opcode[i] <= 1943:

                self.instrSpaced.append(SetUp.bin2StringSpacedIM(instructions[i]))
                self.opcodeStr.append("MOVK")

                # 3rd data field
                self.arg1.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg2.append((int(instructions[i], base=2) & MASKs.imdataMask) >> 5)

                # bitshift 17 because its result * 16
                self.arg3.append((int(instructions[i], base=2) & MASKs.imsftMask) >> 17)

                # MOVK R2, 65280, LSL 48
                self.arg1Str.append("\tR" + str(self.arg1[i]))
                self.arg2Str.append(", " + str(self.arg2[i]))
                self.arg3Str.append(", LSL " + str(self.arg3[i]))



            # LSR R0, R1, #4  Type R
            elif opcode[i] == 1690:

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("LSR")

                self.arg1.append((int(instructions[i], base=2) & MASKs.shmtMask) >> 10)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg1[i]))

                #NEWLY ADDED
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg2[i])

                # LSL R0, R1, #4  Type R
            elif opcode[i] == 1691:

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("LSL")

                self.arg1.append((int(instructions[i], base=2) & MASKs.shmtMask) >> 10)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg1[i]))

                ##NEWLY ADDED
                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(-19)
                #self.destReg.append(self.arg1[i])
                #self.src1Reg.append(self.arg2[i])
                #self.src2Reg.append(-11)

                # ASR R0, R1, #4  Type R
            elif opcode[i] == 1692:

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ASR")

                self.arg1.append((int(instructions[i], base=2) & MASKs.shmtMask) >> 10)
                # self.arg1.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & MASKs.shmtMask) >> 10), 6))

                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                # self.arg2.append(SetUp.imm_bit_to_32_bit_converter(((int(instructions[i], base=2) & MASKs.rnMask) >> 5), 5))

                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                # self.arg1.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                # self.arg2.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)
                # self.arg3.append(0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg2[i]))
                self.arg3Str.append(", #" + str(self.arg1[i]))

                # self.arg1Str.append("\tR" + str(self.arg2[i]))
                # self.arg2Str.append(", R" + str(self.arg1[i]))
                # self.arg3Str.append("")


            # EOR #R3, R1, R2
            elif opcode[i] == 1872:

                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("EOR")

                self.arg1.append((int(instructions[i], base=2) & MASKs.rmMask) >> 16)
                self.arg2.append((int(instructions[i], base=2) & MASKs.rnMask) >> 5)
                self.arg3.append((int(instructions[i], base=2) & MASKs.rdMask) >> 0)

                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg2[i]))
                self.arg3Str.append(", R" + str(self.arg1[i]))

                self.destReg.append(self.arg3[i])
                self.src1Reg.append(self.arg2[i])
                self.src2Reg.append(self.arg1[i])


            # NOP
            elif opcode[i] == 0:

                self.instrSpaced.append(SetUp.bin2StringSpaced(instructions[i]))
                self.opcodeStr.append("NOP")

                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)

                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")




            elif opcode[i] == 2038 and (int(instructions[i], base=2) & MASKs.specialMask) == 2031591:
                self.instrSpaced.append(SetUp.bin2StringSpaced(instructions[i]))
                self.opcodeStr.append("BREAK")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print
                "breaking"
                break
            else:
                self.opcodeStr.append("unknown")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print("i =:  " + str(i))  # correct amt of space?
                print("opcode =:  " + str(opcode[i]))
                sys.exit("You have found an unknown instruction, investigate NOW")

        for i in range(self.numInstructs, len(instructions)):
            # self.address.append(96 + (self.numInstructs * 4) + (i * 4))
            # print("appending address:")
            # print(self.address[-1])
            self.rawdata.append(instructions[i])
            self.dataval.append(SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(int(instructions[i], base=2)))

        # ***
        return {
            "instructions": instructions,
            "opcode": opcode,
            "opcodeStr": self.opcodeStr,
            "arg1": self.arg1,
            "arg1Str": self.arg1Str,
            "arg2": self.arg2,
            "arg2Str": self.arg2Str,
            "arg3": self.arg3,
            "arg3Str": self.arg3Str,
            "dataval": self.dataval,
            "address": self.address,
            "numInstructs": self.numInstructs,
            "destReg": self.destReg,
            "src1Reg": self.src1Reg,
            "src2Reg": self.src2Reg}

    def print(self):
        outFile = open(SetUp.get_output_filename() + "_dis.txt", 'w')

        for i in range(self.numInstructs):
            outFile.write(str(self.instrSpaced[i]) + '\t' + str(self.address[i]) +
                          '\t' + str(self.opcodeStr[i]) + str(self.arg1Str[i]) +
                          str(self.arg2Str[i]) + str(self.arg3Str[i]) + '\n')

        for i in range(len(self.dataval)):
            outFile.write(str(self.rawdata[i]) + '\t' + str(self.address[i + self.numInstructs]) + \
                          '\t' + str(self.dataval[i]) + '\n')

        outFile.close()





