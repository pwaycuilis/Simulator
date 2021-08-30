
import simClass

class WriteBack:

    def __init__(self, R, postMemBuff,postALUBuff, destReg):
        self.R = R

        self.postMemBuff = postMemBuff
        self.postALUBuff = postALUBuff
        self.destReg = destReg


    def run(self):

        print(f"(writeBack16)self.destReg : {self.destReg}")
        #print(f"(WB17)self.src1Reg : {self.src1Reg}")
        #print(f"(WB17)self.src2Reg : {self.src2Reg}")

        print(f"(WB18)self.postALUBuff[1] : {self.postALUBuff[1]}")
        #print(f"self.R[self.destReg[self.postALUBuff[1]]] : {self.R[self.destReg[self.postALUBuff[1]]]}")
        print(f"(WB20)self.postALUBuff[0]: {self.postALUBuff[0]}")
        if self.postMemBuff != [-1, -1]:
            self.R[self.destReg[self.postMemBuff[1]]] = self.postMemBuff[0]  #self.R[self.destReg[
            self.postMemBuff = [-1, -1]
            print(f"(WB24)self.postMemBuff = {self.postMemBuff}")



        #if postALUBuff not empty, write value to register and then clear buff

        if self.postALUBuff != [-1, -1]:
            self.R[self.destReg[self.postALUBuff[1]]] = self.postALUBuff[0]
            self.postALUBuff = [-1, -1]

        # if self.postMemBuff[1] != -1:
        #     self.R[self.destReg[self.postMemBuff[1]]] = self.postMemBuff[0]
        #
        #     self.postMemBuff[0] = -1
        #     self.postMemBuff[1] = -1
        #
        # if self.postALUBuff[1] != -1:
        #     self.R[self.destReg[self.postALUBuff[1]]] = self.postALUBuff[0]
        #
        #     self.postALUBuff[0] = -1
        #     self.postALUBuff[1] = -1

        # print("in Writeback: R, postMemBuff, postALUBuff, destReg")
        # print(self.R)
        # print(self.postMemBuff)
        # print(self.postALUBuff)
        # print(self.destReg)

        #orignally uncommented**************VVVV
        #return WriteBack(self.R, self.postMemBuff, self.postALUBuff, self.destReg)
        #**********************************^^^^^^
        return [self.R, self.postMemBuff, self.postALUBuff, self.destReg]
        #return [self.R, self.postMemBuff, self.postALUBuff]

    # def updateBuffer(self):
    #     return [self.R, self.postMemBuff, self.postALUBuff]
        #print(f"in writeback self.R: {self.R}")
        #return self.R
        # print(postMemBuff)
        # print(postALUBuff)

