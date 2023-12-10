: 0
;;; DATA
_arithmetic_counter ffff
# _arithmetic_counter 0
_arithmetic_buffer fffe
# _arithmetic_buffer 0
_addl_arithmetic_buffer fffd
# _addl_arithmetic_buffer 0
_one fffc
# _one 1
_zero fffb
# _zero 0
;;;
;;; FUNCTIONS
;;;;
JMP 30
;
; Multiplies A x B
;
.multiply
; Zero the counter 
PHA 0000
LDA _zero
STA _arithmetic_counter
BTA 0000
SBA _one ; Decrement B by one so we count properly
ATB 0000
PLA 0000
; Move values to useable locations
STB _arithmetic_buffer
STA _addl_arithmetic_buffer
; Add A to itself B times
.m_loop
ADA _addl_arithmetic_buffer ; A = A + A
PHA 0000
LDA _arithmetic_counter ; Increment Counter
ADA _one
STA _arithmetic_counter
LDT _arithmetic_buffer
UFR 0000
PLA 0000
BNE .m_loop ; If we haven't added A+A B times, loop
RST 0000 ; If we have, we're done
;
; Adds A + B
;
.add
STB _arithmetic_buffer
ADA _arithmetic_buffer
RST 0000
_prompt fff9
# _prompt %>
_space fff8
# _space 20
_a fff7
_b fff6
_conv fff5
# _conv 30
_plus fff4
# _plus %+
_mult fff3
# _mult %*
_op fff2
_err fff1
# _err %x
_eq fff0
# _eq %=
_n ffef
# _n a
.print_prompt
; Print input prompt
LDA _prompt
ATO 0000
RST 0000
.input
RIR _arithmetic_buffer
LDA _arithmetic_buffer
LDT _zero
UFR 0000
BEQ .input ; If input is nothing, wait for input
RST 0000
.perform_add
LDA _a
LDB _b
JST .add
ADA _conv ; convert from integer to character
ATO 0000 ; output
LDA _n
ATO 0000
JMP 30 ; main
.perform_mult
LDA _a
LDB _b
JST .multiply
ADA _conv
ATO 0000
LDA _n
ATO 0000
JMP 30 ; main
;;;
;;; MAIN
;;;
JST .print_prompt
JST .input ; store first charcter in register A
ATO 0000
PHA 0000
LDA _space
ATO 0000
PLA 0000
SBA _conv ; convert from character to integer
STA _a
JST .input ; get operand
STA _op
ATO 0000
PHA 0000
LDA _space
ATO 0000
PLA 0000
JST .input
ATO 0000
PHA 0000
LDA _space
ATO 0000
LDA _eq
ATO 0000
LDA _space
ATO 0000
PLA 0000
SBA _conv
STA _b
; Determine operation
LDA _op
LDT _plus
UFR 0000
BEQ .perform_add
LDT _mult
UFR 0000
BEQ .perform_mult
LDA _err
AOT 0000
HLT 0000
