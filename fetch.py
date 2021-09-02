
import cache


class Fetch:

    totalFetched = 0
    totalChecked = 0
    #rTypeInBuff = 0
    def __init__(self, preIssueBuff, instruction, opcodes, opcodeStr, dataval, address,
                 arg1, arg2, arg3, numInstrs, destReg, src1Reg, src2Reg):

        self.instruction = instruction
        self.opcodes = opcodes
        self.opcodeStr = opcodeStr
        self.dataval = dataval
        self.address = address
        self.arg1 = arg1
        self.arg2 = arg2
        self.arg3 = arg3
        self.numInstrs = numInstrs
        self.destReg = destReg
        self.src1Reg = src1Reg
        self.src2Reg = src2Reg

        self.cache = cache.Cache(numInstrs, instruction, dataval, address)

        # print(self.opcodeStr)

        self.preIssueBuff = preIssueBuff

    def run(self):
        """
        IF can fetch and decode up to two instr per cycle
        instructions are fetched and decoded in program order
        conditions to be met before instructions can be fetched
        1. If fetch unit is stalled, no instructions can be fetched at curr cycle
        (can be stalled due to branch instruction or cache miss
        2. If there is no room in pre-issue buff
        3. If there is only one empty slot in pre-issue buffer, only one instruction will be fteched
        :return:
        """
        foundBreak = False

        fetchesPerCycle = 0

        #while foundBreak == False
        numInBuff = 0

        readyToCycle = True

        rTypeInBuff = 0


        for i in range(len(self.preIssueBuff)):
            if self.preIssueBuff[i] > -1:
                numInBuff += 1
               

       
        if fetchesPerCycle < 2 and numInBuff < 4 and readyToCycle:
            for i in range(self.totalFetched, (len(self.instruction))):
                
                #if self.cache.checkCache(-1, i, 0, 0):  #If passing instr index, pass -1 for data index
                readyToCycle = self.cache.checkCache(-1, i, 0, 0)
                if readyToCycle[0]:
    
                    self.addToBuff(i)
                    fetchesPerCycle += 1
                    numInBuff += 1
                    self.totalFetched += 1
                    rTypeInBuff += 1
                    break  #added else 8/8
                else:
                    readyToCycle = False

                    break

   
            #do again to get 2 fetches per cycle
        #if fetchesPerCycle < 2 and numInBuff < 4:
        if fetchesPerCycle < 2 and numInBuff < 4 and readyToCycle:
            for i in range(self.totalFetched, (len(self.instruction))):
            
                #if self.cache.checkCache(-1, i, 0, 0):  #If passing instr index, pass -1 for data index
                #if self.cache.checkCache(i, i, 0, self.dataval):
                [readyToCycle, checkCacheNum] = self.cache.checkCache(-1, i, 0, 0)
             
                if readyToCycle:
                    self.addToBuff(i)
                    fetchesPerCycle += 1
                    numInBuff += 1
                    self.totalFetched += 1
                    rTypeInBuff += 1
                    break #added else 8/8
                else:
                    readyToCycle = False
              
                    break

        #testing ( to sort preissue buff in order)
        for i in range(len(self.preIssueBuff)):
            for j in range(0, len(self.preIssueBuff)-i-1):
                if (self.preIssueBuff[j] > self.preIssueBuff[j+1]) and self.preIssueBuff[j+1] != -1:
                    self.preIssueBuff[j], self.preIssueBuff[j+1] = self.preIssueBuff[j+1], self.preIssueBuff[j]

  
  


        return self.preIssueBuff



        #(instruction, opcodes, opcodeStr, dataval, address, arg1, arg2, arg3,
         #                          numInstrs, destReg, src1Reg, src2Reg)

    def addToBuff(self, n):
        for i in range(len(self.preIssueBuff)):
          
            if self.preIssueBuff[i] < 0:
              
                self.preIssueBuff[i] = n
                break

