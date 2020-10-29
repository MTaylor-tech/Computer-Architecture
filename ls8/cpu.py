"""CPU functionality."""

import sys

# Opcodes
OP = "op"
OANDS = "operands"
TP = "type"
OPCODES = {
    0b10100000: {OP:"ADD",OANDS:2,TP:1},
    0b10101000: {OP:"AND",OANDS:2,TP:1},
    0b01010000: {OP:"CALL",OANDS:1,TP:2},
    0b10100111: {OP:"CMP",OANDS:2,TP:1},
    0b01100110: {OP:"DEC",OANDS:1,TP:1},
    0b10100011: {OP:"DIV",OANDS:2,TP:1},
    0b00000001: {OP:"HLT",OANDS:0,TP:0},
    0b01100101: {OP:"INC",OANDS:1,TP:1},
    0b01010010: {OP:"INT",OANDS:1,TP:2},
    0b00010011: {OP:"IRET",OANDS:0,TP:2},
    0b01010101: {OP:"JEQ",OANDS:1,TP:2},
    0b01011010: {OP:"JGE",OANDS:1,TP:2},
    0b01010111: {OP:"JGT",OANDS:1,TP:2},
    0b01011001: {OP:"JLE",OANDS:1,TP:2},
    0b01011000: {OP:"JLT",OANDS:1,TP:2},
    0b01010100: {OP:"JMP",OANDS:1,TP:2},
    0b01010110: {OP:"JNE",OANDS:1,TP:2},
    0b10000011: {OP:"LD",OANDS:2,TP:0},
    0b10000010: {OP:"LDI",OANDS:2,TP:0},
    0b10100100: {OP:"MOD",OANDS:2,TP:1},
    0b10100010: {OP:"MUL",OANDS:2,TP:1},
    0b00000000: {OP:"NOP",OANDS:0,TP:0},
    0b01101001: {OP:"NOT",OANDS:1,TP:1},
    0b10101010: {OP:"OR",OANDS:2,TP:1},
    0b01000110: {OP:"POP",OANDS:1,TP:0},
    0b01001000: {OP:"PRA",OANDS:1,TP:0},
    0b01000111: {OP:"PRN",OANDS:1,TP:0},
    0b01000101: {OP:"PUSH",OANDS:1,TP:0},
    0b00010001: {OP:"RET",OANDS:0,TP:2},
    0b10101100: {OP:"SHL",OANDS:2,TP:1},
    0b10101101: {OP:"SHR",OANDS:2,TP:1},
    0b10000100: {OP:"ST",OANDS:2,TP:0},
    0b10100001: {OP:"SUB",OANDS:2,TP:1},
    0b10101011: {OP:"XOR",OANDS:2,TP:1}
}

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0b00000000]*256
        self.reg = [0b00000000]*8
        self.pc = 0 #program counter
        self.running = True

    def ram_read(self,address):
        if address < len(self.ram):
            return self.ram[address]
        else:
            raise Exception("RAM (read) address out of bounds")


    def ram_write(self,address,value):
        if address < len(self.ram):
            self.ram[address] = value
        else:
            raise Exception("RAM (write) address out of bounds")


    def load(self,filename):
        """Load a program into memory."""
        address = 0
        program = []
        with open(filename,"r") as f:
            for line in f:
                line = line.partition('#')[0]
                line = line.rstrip()
                if line != '':
                    program.append(int(line,base=2))
        for instruction in program:
            self.ram_write(address,instruction)
            address += 1


    def process(self, op, operand_a, operand_b):
        if op == "HLT": # HALT
            self.running = False
            return
        elif op == "LDI": # Load immediate: save value to a register
            self.reg[operand_a] = operand_b
            self.pc += 3
        elif op == "PRN":
            print(self.reg[operand_a])
            self.pc += 2
        else:
            raise Exception("Unsupported operation")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD": # ADD the value of register b to the val of reg a
            self.reg[reg_a] = (self.reg[reg_a]+self.reg[reg_b])&0xFF
            # self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "MUL": # MULtiply the value of register b to the val of reg a
            self.reg[reg_a] = (self.reg[reg_a]*self.reg[reg_b])&0xFF
            # self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


# if (x & (1<<n))
#   ## n-th bit is set (1)
#
# else
#   ## n-th bit is not set (0)
    def run(self):
        """Run the CPU."""
        while self.running:
            op_code = self.ram_read(self.pc)
            instruction = OPCODES.get(op_code)
            if instruction is not None:
                if instruction[TP]==1:
                    self.alu(instruction[OP],self.ram_read(self.pc+1),self.ram_read(self.pc+2))
                else:
                    self.process(instruction[OP],self.ram_read(self.pc+1),self.ram_read(self.pc+2))
            else:
                raise Exception("Unrecognized OP Code")
