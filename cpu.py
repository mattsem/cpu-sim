r1 = [1]*16
r2 = [0]*16
r3 = [0]*16
r4 = [0]*16

regs = {'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4}

def readInst():
    inst = None
    while inst != 'end':
        inst = input('enter instruction:\n')
        #print(inst)
        if inst.split()[0] == 'add':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = add(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'addi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = add(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))



def add(reg1, reg2):
    result = [0]*16
    print('adding')
    print(binToDec(reg1),' = ', binToDec(reg1) ,' + ' , binToDec(reg2))
    carry = 0
    sum = 0 
    #big endian so traverse in reverse
    for index in range(len(reg1)-1,-1,-1):
        sum = reg1[index] + reg2[index] + carry
        if sum == 0:
            result[index] = 0
            carry = 0
        elif sum == 1:
            result[index] = 1
            carry = 0
        elif sum == 2:
            result[index] = 0
            carry = 1
        elif sum == 3:
            result[index] = 1
            carry = 1
    return result


def binToDec(reg):
    dec = 0
    for num in reg:
        dec = (2*dec)+num
    return dec

def decToBin(dec):
    bin = [0]*16
    for index in range(15,-1,-1):
        bit = dec % 2
        bin[index] = bit
        dec//=2
    return bin


#print(decToBin(1))
readInst()