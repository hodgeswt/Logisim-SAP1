: 0
_one ffff
# _one 1
_zero fffe
# _zero 0
_counter fffd
# _counter 0
_buffer fffc
# _buffer 0
_cr fffb
# _cr 0a
_inp_p fffa
# _inp_p fff9
JMP 4
.end
LDA _counter
AOT 0000
HLT 0000
;;; MAIN
ADI _inp_p
.inp_loop
RIR _buffer
LDA _buffer
LT _zero
UFR 0000
BEQ .inp_loop ; Wait for input
LT _cr
UFR 0000
BEQ .end ; If end of input, do smth else
TAD 0000 ; Otherwise save at pointer
ARD 0000 ; Decrement pointer
LDA _counter ; And count up one
ADA _one
STA _counter
JMP .inp_loop ; Wait for more input
