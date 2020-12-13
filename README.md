# WH-01
8-bit CPU built in Logisim

# To Use
- Download the repository and open logisim-evolution-3.3.6-all.jar
- Inside Logisim Evolution, open WH01.circ
- Right click on Control_Logic and select "Load Image"
- Load ctrl_logic.bin
- Using the poke tool, double click on RAM
- Right click on the RAM module and select "Load Image"
- Load "out.bin"
- Return to main circuit
- Enable ticks

# To program
- Opcode list:
	- NOP : no operation
	- LDA hh : loads A register with value stored at memory address operand
	- ROT : Outputs value at current RAM address to output register 1
	- AOT : Outputs A register to output register 1
	- JMP hh : Unconditional jump to provided address
	- HLT : halt execution
	- ADA hh : adds value at provided memory address into A register
	- SBA hh : subtracts value from provided memory address from A register
	- STA hh : Stores A register value at provided memory address
	- LDB hh : Loads B register with value stored at operand
	- BOT hh : Outputs B register to provided memory address
	- LDC hh : Loads C register
	- COT hh : Output C register to output register 1
	- STB hh : Stores B register at provided memory address
	- BEQ hh : Branches to provided address if A and TMP registers were equal when flags were last updated
	- BNE hh : Branches to address if A and TMP not equal at last flag update
	- UFR    : Updates flag register
	- BZO hh : Branches if A + TMP = 0
	- PHA    : Pushes A register onto stack
	- PLA    : Pulls A off of stack
	- JST hh : Jumps to subroutine at provided address
	- RST    : Returns from subroutine and continues at JST +1
	- BTA    : Moves B register to A
	- CTA    : C -> A
	- ATB    : A -> B
	- ATC    : A -> C
	- LT  hh : Loads TMP register with value at address
	- ATO    : Output A to Output Register 2
	- BTO    : Output B to Output Register 2
	- LBA    : Loads A register with value at memory address stored in register B
- Anything that takes no operand should receive operand value 00
- To place a string in memory: `& [starting address] "contents of string"`
	- String is written backwards in memory
- Comments begin with ; and can occur on line of their own or at the end of a line (after op + operand)
- To change the starting address, use `: [address]`

# To assemble
`python3 assembler.py [filename] 256`
	- Outputs file to out.bin 
