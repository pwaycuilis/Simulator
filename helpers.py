import sys


class SetUp:
    def __init__(self):
        pass

        #wbAddr = address of mem to write data
    #SetUp.getIndexOfMemAddress(wbAddr, False, self.dataval, self.address, self.numInstructions)

    #copied from powerpoint

    #def getIndexOfMemAddress(cls, currAddr, isSW, dataval, address, numInstructions):
    def getIndexOfMemAddress(currAddr, isSW, dataval, address, numInstructions):

        tempIndex = 0
        try:
            if isSW:
                # make sure that there is enough spaces in dataval
                #there has to be an even number of elements in dataval

                #if the length of the address list is greater than num instructions
                if len(address) > numInstructions:
                    lastInstructAddr = ((numInstructions - 1) * 4) + 96
                                            # lastMemAddr= lastInstructAddr + 4*(len(address)-self.numInstructions)
                    lastMemAddr = lastInstructAddr + 4 * len(dataval)
                    if currAddr == lastMemAddr:
                        dataval.append(0)
                        dataval.append(0)
                        address.append(lastMemAddr + 4)
                        address.append(lastMemAddr + 8)
                        # add at least one more dataval address space

                    if currAddr > lastMemAddr:
                        addIndex = (currAddr - lastMemAddr) / 4
                        for i in range(int(addIndex)):
                            dataval.append(0)
                            address.append(lastMemAddr + (4 *(i + 1)))
                tmpIndex = address.index(currAddr)
                tmpIndex = tmpIndex - numInstructions # + 1

            else:
                tmpIndex = address.index(currAddr)

                if tmpIndex >= numInstructions:
                    tmpIndex = tmpIndex - numInstructions # + 1

            return tmpIndex
        except ValueError:
            print("ERROR -- did not find mem address currAddr " + str(currAddr))

        #end of copied from powerpoint


    #PRIOR getIndexOfMemAddress
    """
    def getIndexOfMemAddress(wbAddr, trueOrFalse, dataval, address, numInstructions):

                                # print(f"wbAddr:{wbAddr}")
                                # print(dataval)
                                # print(address)
                                # print(numInstructions)

        if trueOrFalse == False:
            memIndex = (wbAddr - 96) // 4
                                # print(f"address1 or wbAddr:{wbAddr}")
                                # print(f"address list:{address}")
                                # print(f"memIndex from helpers:{memIndex}")
            return memIndex

        else:
            return 0





        return memIndex

    """

    @classmethod
    def get_input_filename(cls):
        # gets input file name from cmd line and returns name

        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
                print(inputFileName)
        # *************
        return inputFileName
        # return "branchtest_bin.txt"

    @classmethod
    def get_output_filename(cls):
        # gets output file name from cmd line and returns name
        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-o' and i < (len(sys.argv) - 1)):
                outputFileName = sys.argv[i + 1]
        # ************
        return outputFileName
        # return "test.txt"

    @classmethod
    def import_data_file(cls):
        # gets file name from cmd line then downloads input file and returns list
        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]

        try:
            # **************
            instructions = [line.rstrip() for line in open(inputFileName, 'r')]
            # instructions = [line.rstrip() for line in open("machLang.txt", 'r')]
            # instructions = [line.rstrip() for line in open("branchtest_bin.txt", 'r')]
        except IOError:
            print("Could not open input file, is path correct?")

        return instructions

    # slide 45
    @classmethod
    def imm_bit_to_32_bit_converter(cls, num, bitsize):
        # Converts binaries of various lengths to a standard 32 bit length

        # and : returns the converted number     #supposed to be commented out?

        negBitMask = 2 ** (bitsize - 1)
        # print(hex(negBitMask))

        extendMask = (2 ** 32) - negBitMask
        # print(hex(num))
        # print(hex(extendMask))

        if (negBitMask & num) > 0:  # is it?
            num = num | extendMask  # if so extend with 1's

            num = num ^ 0xFFFFFFFF  # 2s comp
            num = num + 1
            num = num * -1  # add neg sign
            # print(hex(num))
        return num

    ##    @classmethod
    ##    def immSignedToTwosConverter(cls,num):
    ##
    # .............

    @classmethod
    def bin2StringSpaced(cls, s):
        spacedStr = s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:26] + " " + s[26:32]
        return spacedStr

    # for LDUR and STUR
    @classmethod
    def bin2StringSpacedD(cls, s):
        # ........
        spacedStr = s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + \
                    s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedIM(cls, s):
        spacedStr = s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + \
                    s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedCB(cls, s):
        spacedStr = s[0:8] + " " + s[8:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedI(cls, s):

        spacedStr = s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedR(cls, s):

        spacedStr = s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStr

    @classmethod
    def bin2StringSpacedB(cls, s):

        spacedStr = s[0:6] + " " + s[6:32]
        return spacedStr

    @classmethod
    def imm_32_bit_unsigned_to_32_bit_signed_converter(cls, num):
        # converts 32 bit signed, handles negative numbers, returns number

        negBitMask = 2 ** 31

        extendMask = (2 ** 32) - negBitMask

        if (negBitMask & num) > 0:  # is it?
            num = num | extendMask  # if so extend with 1's

            num = num ^ 0xFFFFFFFF  # 2s comp
            num = num + 1
            num = num * -1  # add neg sign
            # print(hex(num))

        return num  # eventually convert this to decimal for display

    @classmethod
    def decimalToBinary(cls, num):
        # This functions converts decimal number to binary and prints it

        if num > 1:
            cls.decimalToBinary(num // 2)
        print(num % 2, end='')

    @classmethod
    def binaryToDecimal(cls, binary):
        print("\n")
        print(int(binary, 2))


