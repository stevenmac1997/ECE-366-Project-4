def hexToBin (line):
    newLine = 0
    for i in range(0, len(line)):
        #print("Line: " + line[len(line) - i -1] + "\t# of chars:"+ str(len(line)))

        if(line[len(line) - i -1] == 'A' or line[len(line) - i -1] == 'a'):
            newLine += 10 * (16 ** i)
        elif(line[len(line) - i -1] == 'B' or line[len(line) - i -1] == 'b'):
            newLine += 11 * (16 ** i)
        elif (line[len(line) - i -1] == 'C' or line[len(line) - i -1] == 'c'):
            newLine += 12 * (16 ** i)
        elif (line[len(line) - i -1] == 'D' or line[len(line) - i -1] == 'd'):
            newLine += 13 * (16 ** i)
        elif (line[len(line) - i -1] == 'E' or line[len(line) - i -1] == 'e'):
            newLine += 14 * (16 ** i)
        elif (line[len(line) - i -1] == 'F' or line[len(line) - i -1] == 'f'):
            newLine += 15 * (16 ** i)
        else:
            newLine += int(line[len(line) - i -1]) * (16**i)
    #print(str(newLine))
    newLine = format(int(newLine), "b")
    return newLine.rjust(32, '0')

def simulate(instr, output):
    DIC = 0 #Dynamic Instruction Count
    Reg = [0, 0, 0, 0, 0, 0, 0, 0] #Registers $0 to $7
    Mem = [0] * 512 #Memory Addresses, each initialized at 0
    PC = 0 #Program Counter
    finished = False
    while(not(finished)):
            line = instr[PC]
            #print(line)
            DIC += 1
            if(line[0:6] == "000000"):
                if(line[26:32] == "100000"):
                  function = "add"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  Reg[rd] = Reg[rs] + Reg[rt]
                  PC += 1
                  #print (str(function) + " " + str(rd) + "," + str(rs) + "," + str (rt))
                elif(line[26:32] == "100010"):
                  function = "sub"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  Reg[rd]=Reg[rs]-Reg[rt]
                  PC += 1
                  #print (function," ",rd,",",rs,",",rt)
                elif(line[26:32] == "100110"):
                  function = "xor"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  Reg[rd]=Reg[rs]^Reg[rt]
                  PC += 1
                  #print (function," ",rd,",",rs,",",rt)
                elif(line[26:32] == "101010"):
                  function = "slt"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  if (Reg[rs] < Reg[rt]):
                       Reg[rd]=1
                  else:
                       Reg[rd]=0
                  PC += 1
                  #print (function," ",rd,",",rs,",",rt)
            elif(line[0:6] == "001000"):
                function = "addi"
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if(line[16] == "1"):
                    imm = imm - 65536
                #print(imm)
                Reg[rt]=Reg[rs]+imm
                PC +=1
                #print (function," ",rt,",",rs,",",imm)
            elif(line[0:6] == "000100"):
                function = "beq"
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (line[16] == "1"):
                    imm = imm - 65536
                if(Reg[rs] == Reg[rt]):
                    addThis = imm + 1
                else:
                    addThis = 1
                if(addThis != 0):
                    PC += addThis
                else:
                    finished = True
                #print (str(function) + " " + str(rt) + "," + str(rs) + "," + str(imm))
            elif(line[0:6] == "000101"):
                function = "bne"
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if(line[16] == "1"):
                    imm = imm - 65536
                if (Reg[rs] == Reg[rt]):
                    addThis = imm + 1
                else:
                    addThis = 1
                if (addThis != 0):
                    PC += addThis
                else:
                    finished = True
                #print (str(function) + " " + str(rt) + "," + str(rs) +"," + str(imm))
            elif(line[0:6] == "100011"):
                function = "lw"
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (line[16] == "1"):
                    imm = imm - 65536
                imm = imm - 8192

                Reg[rt]=Mem[Reg[rs]+imm]
                PC +=1
                #print (function," ",rt,",",rs,",",imm)
            elif(line[0:6] == "101011"):
                function = "sw"
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                #if (line[16] == "1"):
                #    imm = imm - 65536
                imm = imm - 8192
                Mem[Reg[rs]+imm]=Reg[rt]
                PC +=1
                #print (function," ",rt,",",rs,",",imm)
    print("\nReg: " + str(Reg))
    print("PC: " + str(PC + 1))
    print("DIC: " + str(DIC))
    output.write("Reg: " + str(Reg))
    output.write("\nPC : " + str(PC+1))
    output.write("\nDIC: " + str(DIC))


def main():
    print("ECE366 Fall 2018: MIPS Mini Assembler")
    print("\nMembers:")
    print("Francis Paul Amadeo")
    print("Steven Mac\n\n")

    #VARIABLES:
    Nlines = 0  # Number of lines
    instr =[] #Instructions will be here

    print("Reading in instruction file...")
    inFile = open("i_mem.txt", "r")
    outFile = open("output.txt", "w")

    for line in inFile:
        if (line == "\n"):
            continue
        line = line.replace("\n", "")
        line = line.replace("0x", "")
        instr.append(hexToBin(line))  # Copy all instruction into a list
        Nlines += 1

    print("...finished reading in instruction file")
    print("\nSimulating...")
    simulate(instr, outFile)
    print("\nSimulation done")

    inFile.close()
    outFile.close()

    exit()


if __name__ == "__main__":
    main()
