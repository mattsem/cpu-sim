#main memory
cols,rows = 16,16

mem = [[0]*cols]*rows
#print(mem)


#instr memory
global instrMem
global pc
pc = [0]*16



#registers
r0 = [0]*16
r1 = [1]*16
r2 = [0]*16
r3 = [0]*16
r4 = [0]*16
rr = [0]*16

regs = {'r0': r0,'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4,'rr':rr}

#r0 always zero
freeRegs = [1,1,0,0,0]


functions = {}

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

        if inst.split()[0] == 'sub':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = sub(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'subi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = sub(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'mul':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = naiveMul(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'print':
            printRegs()

        if inst.split()[0] == 'load':
            p1 = inst.split()[1]
            memory = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            regs[p1] = load(regs[p1],int(memory))
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'store':
            memory = inst.split()[1]
            p1 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            store(int(memory),regs[p1])

        if inst.split()[0] == 'read':
            readFile()

        if inst.split()[0] == 'run':
            runFile()

        if inst.split()[0] == 'jump':
            jump(inst.split()[1])

        if inst.split()[0] == 'beq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchEq(regs[p1],regs[p2],int(addr))

        if inst.split()[0] == 'bnq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchNeq(regs[p1],regs[p2],int(addr))
       
        

    printRegs()

def add(reg1, reg2):
    result = [0]*16
    print('adding')
    print(binToDec(reg1),' = ', binToDec(reg1) ,' + ' , binToDec(reg2))
    carry = 0
    sum = 0 
    #big endian so traverse in reverse
    for index in range(15,-1,-1):
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

def sub(reg1,reg2):
    result = [0]*16
    print('subbing')
    print(binToDec(reg1),' = ', binToDec(reg1) ,' - ' , binToDec(reg2))
    borrow = 0
    diff = 0

    for index in range(15,-1,-1):
        diff = reg1[index] - reg2[index] - borrow
        if diff == 0:
            result[index] = 0
            borrow = 0
        elif diff == 1:
            result[index] = 1
            borrow = 0
        elif diff == -1:
            result[index] = 1
            borrow = 1
        elif diff == -2:
            result[index] = 0
            borrow = 1
    return result


def naiveMul(reg1,reg2):
    print('multiplying')
    print(binToDec(reg1),' = ', binToDec(reg1) ,' * ' , binToDec(reg2))
    result = reg1
    if binToDec(reg2) == 0 or binToDec(reg1) == 0:
        result = decToBin(0)
        return result
    for addition in range(1,binToDec(reg2)):
            result = add(result,reg1)
    return result


def jump(address):
    global pc
    pc = decToBin(address)

def branchEq(reg1,reg2,address):
    if sub(reg1,reg2) == decToBin(0):
        jump(address)
        print('branching to ', address)
    else:
        print('not branching')


def branchNeq(reg1,reg2,address):
    if sub(reg1,reg2) != decToBin(0):
        jump(address)
        print('branching to ', address)
    else:
        print('not branching')

def load(reg, memory):
    print('loading')
    return mem[memory]


def store(memory, reg):
    print('storing')
    mem[memory] = reg
    print(mem)
    printRegs()


def readFile():
    global instrMem
    instructions = open('cpu-sim/instr.txt','r')
    instrMem = [line.strip() for line in instructions]
    instructions.close()
    printInstr()

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


def printRegs():
    for reg in regs:
        print(reg,': ',regs[reg], binToDec(regs[reg]))

def printInstr():
    print(instrMem)


def runFile():
    global pc
    pc = sub(pc,pc)
    while binToDec(pc) != 65535:
        inst = instrMem[binToDec(pc)]
        pc = add(pc,decToBin(1))

        if inst.split()[0] == 'end':
            printRegs()
            pc = decToBin(65535)
        
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

        if inst.split()[0] == 'sub':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = sub(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'subi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = sub(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'mul':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = naiveMul(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'print':
            printRegs()

        if inst.split()[0] == 'load':
            p1 = inst.split()[1]
            memory = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            regs[p1] = load(regs[p1],int(memory))
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'store':
            memory = inst.split()[1]
            p1 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            store(int(memory),regs[p1])

        if inst.split()[0] == 'jump':
            jump(inst.split()[1])
        
        if inst.split()[0] == 'beq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchEq(regs[p1],regs[p2],int(addr))

        if inst.split()[0] == 'bnq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchNeq(regs[p1],regs[p2],int(addr))

        if inst.split()[0] == 'func:':
            functions.update({inst.split()[1] : binToDec(pc)})
            print(functions)

        if inst.split()[0] == 'ret':
            regs['rr'] = regs[inst.split()[1]]
            print(regs['rr'],binToDec(regs['rr']))

        if inst.split()[0] in functions:
            print('jumping to func:',inst.split()[0])
            jump(functions[inst.split()[0]])
            

    print('PROGRAM COMPLETED')


#printRegs()
#print(sub(decToBin(5),decToBin(4)))
#print(decToBin(1))
readInst()