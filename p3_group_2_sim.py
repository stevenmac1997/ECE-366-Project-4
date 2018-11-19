print("Our ISA Simulator")
print("----------")




def simulate(Instr, num_instr, Mem):

    DIC = 0
    Reg = [0,0,0,0]
    PC = 0
    print("***** Simulation Start ******")
    finished = False
    
    while(not(finished)):
        line = Instr[PC]
        DIC += 1

        print (Reg)
        
        if(line[1:4] == "000"):
            funct = "lw"
            rx = int(line[4:6],2)
            ry = int(line[6:8],2)
            Reg[rx] = Mem[Reg[ry]]
            PC += 1
            print("%s $%s, ($%s)" % (funct, rx, ry))
            
        elif(line[1:4] == "001"):
            funct = "sw"
            rx = int(line[4:6],2)
            ry = int(line[6:8],2)
            Mem[Reg[ry]] = Reg[rx]
            PC += 1
            print("%s $%s, ($%s)" % (funct, rx, ry))

        elif(line[1:4] == "010"):
            funct = "add"
            rx = int(line[4:6],2)
            ry = int(line[6:8],2)
            Reg[rx] = Reg[rx] + Reg[ry]
            PC += 1
            print("%s $%s, $%s" % (funct, rx, ry))

        elif(line[1:5] == "0110"):
            funct = "sltR0"
            rx = int(line[5],2)
            ry = int(line[6:8],2)
            if(Reg[rx] < Reg[ry]):
                Reg[0] = 1
            else:
                Reg[0] = 0
            PC += 1
            print("%s $%s, $%s" % (funct, rx, ry))
            
        elif(line[1:8] == "0111000"):
            finished = True
            print('Halt')

        elif(line[1:5] == "0111"):
            funct = "beqz"
            rx = int(line[5],2)
            ry = int(line[6:8],2)
            if(Reg[rx] == 0):
                PC = PC + Reg[ry]
            else:
                PC += 1
            print("%s $%s, $%s" % (funct, rx, ry))
        elif(line[1:4] == "100"):
            funct = "sub"
            rx = int(line[4:6],2)
            ry = int(line[6:8],2)
            Reg[rx] = Reg[rx] - Reg[ry]
            PC += 1
            print("%s $%s, $%s" % (funct, rx, ry))
            
        elif(line[1:4] == "101"):
            funct = "andi"
            rx = int(line[4:6],2)
            ry = int(line[6:8],2)
            Reg[rx] = Reg[ry] & 1
            PC += 1
            print("%s $%s, $%s" % (funct, rx, ry))
            
        elif(line[1:4] == "110"):
            funct = "li"
            rx = int(line[4],2)
            if(line[5] == "1"):
                imm = 0b111 - int(line[5:8],2) + 1 
                Reg[rx] = imm * -1
                PC += 1
                print("%s $%s, -%s" % (funct, rx, imm))
            else:
                imm = int(line[5:8],2)
                Reg[rx] = imm
                PC += 1
                print("%s $%s, %s" % (funct, rx, imm))

        elif(line[1:6] == "11100"):
            funct = "subi"
            rx = int(line[6:8],2)
            Reg[rx] = Reg[rx] - 1
            PC += 1
            print("%s $%s" % (funct, rx))
            
        elif(line[1:6] == "11101"):
            funct = "xorR0"
            rx = int(line[6:8],2)
            Reg[0] = Reg[0] ^ Reg[rx]
            PC += 1
            print("%s $%s" % (funct, rx))
            
        elif(line[1:6] == "11110"):
            funct = "srl"
            rx = int(line[6:8],2)
            Reg[rx] = Reg[rx] >> 1
            PC += 1
            print("%s $%s" % (funct, rx))
            
        elif(line[1:6] == "11111"):
            funct = "jump"
            rx = int(line[6:8],2)
            PC = PC + Reg[rx]
            print("%s $%s" % (funct, rx))
            
        

    print("******** Simulation finished *********")
    print("Dynamic Instr Count: ",DIC)
    print("Registers R0-R3: ",Reg)
    

    data = open("d_mem.txt","w")    # Write data back into d_mem.txt
    for i in range(len(Mem)):
        
        data.write(format(Mem[i],"016b"))
        data.write("\n")
    data.close()


def main():
        instr_file = open("i_mem.txt", "r")
        data_file = open("d_mem.txt", "r")
        Memory = []
        num_instr = 0
        Instruction = []

        print("Group 2's Simulator")

        for line in instr_file:
            if(line == "\n"):
                continue
            line = line.replace("\n","")
            Instruction.append(line)
            num_instr += 1

        for line in data_file:
            if(line == "\n"):
                continue
            line = line.replace("\n","")
            Memory.append(int(line,2))

        simulate(Instruction, num_instr, Memory)

        instr_file.close()
        data_file.close()

if __name__ == "__main__":
    main()
