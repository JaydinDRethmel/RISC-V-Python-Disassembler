# RISC-V-Python-Disassembler
### Details of Project
Created: September 4th, 2026
Created By: Jaydin Rethmel

This project was created as part of an exam for Computer Architecture's Take-Home Exam. The goal of this project is to demonstrate our understanding of machine code and the specifics of Typing within RISC-V assembly code. This program information is detailed within the sections below.

## Details of Program
This Python RISC-V Assembly Disassembler takes a line of hex machine code and converts it into a RISC-V program using its instruction format:
- R-Type: funct7[7-Bits], rs2[5-Bits], rs1[5-Bits], funct3[3-Bits], rd[5-Bits], opcode[7-Bits]
- I-Type: Imm[11:0], rs1[5-Bits], funct3[3-Bits], rd[5-Bits], opcode[7-Bits]
- S-Type: Imm[11:5], rs2[5-Bits], rs1[5-Bits], funct3[3-Bits], Imm[4:0], opcode[7-Bits]
- B-Type: Imm[12|10:5], rs2[5-Bits], rs1[5-Bits], funct3[3-Bits], Imm[4:1], Imm[11], opcode[7-Bits]
- U-Type: Imm[31:12], rd[5-Bits], opcode[7-Bits]
- J-Type: Imm[20|10:1|11|19:12], rd[5-Bits], opcode[7-Bits]

Within this project, a limited scope was imposed to match the level of knowledge that has been taught during lectures from week 1 - week 5 of Fall Semester 2026 (August 24th, 2026 - September 25th, 2026) The Table below shows what assembly code instructions our Disassembler should have within its scope:

| Instruction Category | Instructions |
| :--- | :--- |
| **R-type** | `add`, `sub`, `and`, `or`, `xor`, `sll`, `srl`, `sra`, `slt` |
| **Immediate arithmetic** | `addi`, `andi`, `ori`, `xori`, `slli`, `srli`, `srai` |
| **Memory** | `lw`, `sw` |
| **Branches** | `beq`, `bne`, `blt`, `bge` |
| **Upper/Jumps** | `lui`, `jal`, `jalr` |
