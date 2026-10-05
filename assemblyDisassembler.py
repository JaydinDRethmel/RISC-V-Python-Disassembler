def sign_extend(val, bits):
    """Sign-extends an integer from 'bits' length to 32-bit signed integer."""
    if val & (1 << (bits - 1)):
        val -= (1 << bits)
    return val

def disassemble_rv32i_scope(code_hex):
    """
    Decodes a 32-bit hex machine code string into RISC-V assembly language
    strictly using the required RV32I scope.
    """
    try:
        # Strip potential whitespaces and 0x prefix if user inputs it
        code_hex = code_hex.strip().lower()
        if code_hex.startswith("0x"):
            code_hex = code_hex[2:]
            
        code = int(code_hex, 16)
    except ValueError:
        return "Error: Invalid hexadecimal input."

    # Extract instruction fields
    opcode = code & 0x7F
    rd     = (code >> 7) & 0x1F
    funct3 = (code >> 12) & 0x07
    rs1    = (code >> 15) & 0x1F
    rs2    = (code >> 20) & 0x1F
    funct7 = (code >> 25) & 0x7F

    regs = [f"x{i}" for i in range(32)]

    # 1. R-Type (add, sub, and, or, xor, sll, srl, sra, slt)
    if opcode == 0x33:
        r_ops = {
            (0x00, 0x0): "add", (0x20, 0x0): "sub",
            (0x00, 0x7): "and", (0x00, 0x6): "or",  (0x00, 0x4): "xor",
            (0x00, 0x1): "sll", (0x00, 0x5): "srl", (0x20, 0x5): "sra",
            (0x00, 0x2): "slt"
        }
        mnemonic = r_ops.get((funct7, funct3), "unknown")
        return f"{mnemonic} {regs[rd]}, {regs[rs1]}, {regs[rs2]}"

    # 2. Immediate Arithmetic (addi, andi, ori, xori, slli, srli, srai)
    elif opcode == 0x13:
        imm12 = sign_extend((code >> 20) & 0xFFF, 12)
        shamt = rs2
        if funct3 == 0x1:
            return f"slli {regs[rd]}, {regs[rs1]}, {shamt}"
        elif funct3 == 0x5:
            mnemonic = "srai" if funct7 == 0x20 else "srli"
            return f"{mnemonic} {regs[rd]}, {regs[rs1]}, {shamt}"
        i_ops = {0x0: "addi", 0x7: "andi", 0x6: "ori", 0x4: "xori"}
        mnemonic = i_ops.get(funct3, "unknown")
        return f"{mnemonic} {regs[rd]}, {regs[rs1]}, {imm12}"

    # 3. Memory - Load (lw)
    elif opcode == 0x03 and funct3 == 0x2:
        imm12 = sign_extend((code >> 20) & 0xFFF, 12)
        return f"lw {regs[rd]}, {imm12}({regs[rs1]})"

    # 4. Memory - Store (sw)
    elif opcode == 0x23 and funct3 == 0x2:
        raw_imm = ((code >> 25) << 5) | ((code >> 7) & 0x1F)
        imm12 = sign_extend(raw_imm, 12)
        return f"sw {regs[rs2]}, {imm12}({regs[rs1]})"

    # 5. Branches (beq, bne, blt, bge)
    elif opcode == 0x63:
        raw_imm = (
            ((code >> 31) & 0x1) << 12 |
            ((code >> 7) & 0x1) << 11 |
            ((code >> 25) & 0x3F) << 5 |
            ((code >> 8) & 0xF) << 1
        )
        imm13 = sign_extend(raw_imm, 13)
        b_ops = {0x0: "beq", 0x1: "bne", 0x4: "blt", 0x5: "bge"}
        mnemonic = b_ops.get(funct3, "unknown")
        return f"{mnemonic} {regs[rs1]}, {regs[rs2]}, {imm13}"

    # 6. Upper - LUI (lui)
    elif opcode == 0x37:
        imm20 = (code >> 12) & 0xFFFFF
        return f"lui {regs[rd]}, {imm20}"

    # 7. Jumps - JAL (jal)
    elif opcode == 0x6F:
        raw_imm = (
            ((code >> 31) & 0x1) << 20 |
            ((code >> 12) & 0xFF) << 12 |
            ((code >> 20) & 0x1) << 11 |
            ((code >> 21) & 0x3FF) << 1
        )
        imm21 = sign_extend(raw_imm, 21)
        return f"jal {regs[rd]}, {imm21}"

    # 8. Jumps - JALR (jalr)
    elif opcode == 0x67 and funct3 == 0x0:
        imm12 = sign_extend((code >> 20) & 0xFFF, 12)
        return f"jalr {regs[rd]}, {regs[rs1]}, {imm12}"

    return "Instruction Outside Scope"


# Interactive User Input Loop
if __name__ == "__main__":
    print("=== RISC-V RV32I Scope Disassembler ===")
    print("Enter a 32-bit machine code hex (e.g., '01d28f33' or '0x01d28f33').")
    print("Type 'q' or 'exit' to quit.\n")

    while True:
        user_input = input("Enter Hex Machine Code > ")
        
        if user_input.strip().lower() in ["exit", "q"]:
            print("Exiting disassembler.")
            break
            
        if not user_input.strip():
            continue

        result = disassemble_rv32i_scope(user_input)
        print(f"Assembly Output: {result}\n")