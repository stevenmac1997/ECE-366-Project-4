def hexToBin (line):
    newLine = 0
    for i in range(0, len(line)):
        print("Line: " + line[len(line) - i -1] + "\t# of chars:"+ str(len(line)))

        if(line[len(line) - i -1] == 'A'):
            newLine += 10 * (16 ** i)
        elif(line[len(line) - i -1] == 'B'):
            newLine += 11 * (16 ** i)
        elif (line[len(line) - i -1] == 'C'):
            newLine += 12 * (16 ** i)
        elif (line[len(line) - i -1] == 'D'):
            newLine += 13 * (16 ** i)
        elif (line[len(line) - i -1] == 'E'):
            newLine += 14 * (16 ** i)
        elif (line[len(line) - i -1] == 'F'):
            newLine += 15 * (16 ** i)
        else:
            newLine += int(line[len(line) - i -1]) * (16**i)
    print(str(newLine))
    newLine = format(int(newLine), "b")
    return newLine.rjust(32, '0')

def simulate(instr, output):
    DIC = 0
    Reg = [0, 0, 0, 0, 0, 0, 0, 0]
    PC = 0
    finished = False
    
    while(not(finished)):
            line = instr[PC]
            DIC += 1
            print (Reg,)
            if(line[0:5] == "000000"):
                if(line[26:31] == "100000"):
                  function = "add"
                  rs = int(line[6:10],2)
                  rt = int(line[11:15],2)
                  rd = int(line[15:19],2)
                  Reg[rd]=Reg[rs]+Reg[rt]
                  PC += 1
                  print (function," ",rd,",",rs,",",rt)
                elif(line[26:31] == "100010"):
                  function = "sub"
                  rs = int(line[6:10],2)
                  rt = int(line[11:15],2)
                  rd = int(line[15:19],2)
                  Reg[rd]=Reg[rs]-Reg[rt]
                  PC += 1
                  print (function," ",rd,",",rs,",",rt)
                elif(line[26:31] == "100110"):
                  function = "xor"
                  rs = int(line[6:10],2)
                  rt = int(line[11:15],2)
                  rd = int(line[15:19],2)
                  Reg[rd]=Reg[rs]^Reg[rt]
                  PC += 1
                  print (function," ",rd,",",rs,",",rt)
                elif(line[26:31] == "101010"):
                  function = "slt"
                  rs = int(line[6:10],2)
                  rt = int(line[11:15],2)
                  rd = int(line[15:19],2)
                  if (Reg[rs] < Reg[rt]):
                       Reg[rd]=1
                  else:
                       Reg[rd]=0
                  PC += 1
                  print (function," ",rd,",",rs,",",rt)
            elif(line[0:5] == "001000"):
                function = "addi"
                rs = int(line[6:10],2)
                rt = int(line[11:15],2)
                imm = int(line[16:31],2)
                Reg[rt]=Reg[rs]+imm
                PC +=1
                print (function," ",rt,",",rs,",",imm)
            elif(line[0:5] == "000100"):
                function = "beq"
                rs = int(line[6:10],2)
                rt = int(line[11:15],2)
                imm = int(line[16:31],2)
                if(Reg[rs] == Reg[rt]):
                    PC += imm
                else:
                    PC += 1      
                print (function," ",rt,",",rs,",",imm)
            elif(line[0:5] == "000101"):
                function = "bne"
                rs = int(line[6:10],2)
                rt = int(line[11:15],2)
                imm = int(line[16:31],2)
                if (Reg[rs] == Reg[rt]):
                  PC += 1
                else:
                  PC += imm                 
                print (function," ",rt,",",rs,",",imm)
            elif(line[0:5] == "100011"):
                function = "lw"
                rs = int(line[6:10],2)
                rt = int(line[11:15],2)
                imm = int(line[16:31],2)
                Reg[rt]=Mem[Reg[rs]+imm]
                PC +=1
                print (function," ",rt,",",rs,",",imm)
            elif(line[0:5] == "101011"):
                function = "sw"
                rs = int(line[6:10],2)
                rt = int(line[11:15],2)
                imm = int(line[16:31],2)
                Mem[Reg[rs]+imm]=Reg[rt]
                PC +=1
                print (function," ",rt,",",rs,",",imm)
                                        
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
        instr.append(hexToBin(line))  # Copy all instruction into a list
        Nlines += 1

    print("...finished reading in instruction file")
    print("\nSimulating...")
    simulate(instr, outFile)

    inFile.close()
    outFile.close()

    exit()


if __name__ == "__main__":
    main()
