
class Issue:

    """
    The issue unit follows the basic scoreboaarding algorithm to issue instrucitons.
    It can issue up to two instructions per clock cycle. When an instruction is ussed, it moves out of the pre-issue buffer
    and into either the pre-mem bufeer or the pre-ALU buffer. The issue unit searches from entry 0 to entry 3 of the
    pre-issue buffer and issues instructions if:
    1. No structural  hazard exists.
    2. No RAW hazards exist with active instructions ( all operands are ready)
    3. A load instruction must wait for all previous stores to be issued
    4. Store instructions must be issued in order.

    """
    memIndexOfNext = 96
    currIndex = 0
    def __init__(self, preIssueBuff,preMemBuff, preALUBuff, instructions, opcode, opcodeStr,
                 dataval, address, arg1, arg2, arg3, numInstructs, destReg, src1Reg, src2Reg):
        self.instruction = instructions
        self.opcode = opcode
        self.dataval = dataval
        self.address = address
        self.numInstructions = numInstructs
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg
        self.opcodeStr = opcodeStr
        self.PC = 96
        self.cycle = 1

        self.preIssueBuff = preIssueBuff
        self.preMemBuff = preMemBuff
        self.preALUBuff = preALUBuff

    def run(self):

        numInIssueAtClockCycleBegin = 0
        readyToCycle = True
        
        for i in range(len(self.preIssueBuff)):
            if self.preIssueBuff[i] != -1:
                numInIssueAtClockCycleBegin += 1
                


            ##if current index instr = "ADDI" (or some other valid instr)
            ## and if preALUBuff[0] is empty and preissuebuff[i] == currIndex:
            ##   move contents from preIssueBuff[i] to preALUBuff[0], clear preIssueBuff[i] and currAddr++
            ##elif preALUBuff[1] is empty and preIssueBuff[i] = currIndex:
            ##   move contents from preIssueBuff[i] to preALUBuff[1], clear preIssueBuff[i] and currAddr++

                if readyToCycle and (self.opcodeStr[self.preIssueBuff[i]] == "ADDI" or self.opcodeStr[self.preIssueBuff[i]] == "ADD"\
                        or self.opcodeStr[self.preIssueBuff[i]] == "SUB" or self.opcodeStr[self.preIssueBuff[i]] == "SUBI"\
                        or self.opcodeStr[self.preIssueBuff[i]] == "AND" or self.opcodeStr[self.preIssueBuff[i]] == "ORR"\
                        or self.opcodeStr[self.preIssueBuff[i]] == "EOR" or self.opcodeStr[self.preIssueBuff[i]] == "LSL"):
                    if self.preALUBuff[0] == -1 and self.preIssueBuff[i] == self.currIndex:# and self.address[i] == self.memIndexOfNext:    #and if preALUBuff has open slot
                        print(f"(issue67)self.currIndex : {self.currIndex}")
                        self.preALUBuff[0] = self.preIssueBuff[i]
                        self.preIssueBuff[i] = -1           #set preissuebuff back to -1
                        self.currIndex += 1
                        ## self.memIndexOfNext += 4

                    elif self.preALUBuff[1] == -1 and self.preIssueBuff[i] == self.currIndex:# and self.address[i] == self.memIndexOfNext:
                        print(f"(issue75)self.currIndex : {self.currIndex}")
                        self.preALUBuff[1] = self.preIssueBuff[i]
                        self.preIssueBuff[i] = -1       #set preissuebuff back to -1
                        self.currIndex += 1
                        ## self.memIndexOfNext += 4
                ##added 8/5/21 for STUR/LDUR instructions
                #STUR
                #if src1reg for stur or ldur instruction currently in prealu buff, wait until that register is done

                if self.opcodeStr[self.preIssueBuff[i]] == "STUR" or self.opcodeStr[self.preIssueBuff[i]] == "LDUR":
                   
                    #shuold be self.destReg[self.preIssueBuff[i]]

                    if self.src1Reg[self.preIssueBuff[i]] == (self.destReg[self.preALUBuff[0]] or self.destReg[self.preALUBuff[1]]) and self.src1Reg[self.preIssueBuff[i]] > -1:
                        #changed from src1Reg to src2Reg, need to make condition that both preALUBuffs are not -1 also..
                     
                        readyToCycle = False
                      
                    elif readyToCycle and self.preMemBuff[0] == -1 and self.preIssueBuff[i] == self.currIndex:
                       
                        self.preMemBuff[0] = self.preIssueBuff[i]
                        self.preIssueBuff[i] = -1
                        self.currIndex += 1

                    elif readyToCycle and self.preMemBuff[1] == -1 and self.preIssueBuff[i] == self.currIndex:
                        
                        self.preMemBuff[1] = self.preIssueBuff[i]
                        self.preIssueBuff[i] = -1
                        self.currIndex += 1
               



        #if not readyToCycle:
            #print(f"(issue121)readyToCycle : {readyToCycle} ")


        return [self.preMemBuff, self.preALUBuff, self.preIssueBuff]



