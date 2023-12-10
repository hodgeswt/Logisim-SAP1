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
_prompt fffa
& _prompt "Enter name: "
_prompt_p ffee
# _prompt_p fffa
_p_counter ffed
# _p_counter 0
_p_len ffec
# _p_len 0c
_inp_p ffeb
# _inp_p ffea
JMP 19
.print_char
AIA 0000
ATO 0000
RST 0000
.inc
LDA _p_counter
ADA _one
STA _p_counter
LDT _p_len
UFR 0000
RST 0000
.dec
LDA _counter
SBA _one
STA _counter
LDT _zero
UFR 0000
RST 0000
.end
LDA _counter
ADI _inp_p
.output_loop
JST .print_char
ARD 0000
JST .dec
BNE .output_loop
LDA _zero
STA _counter
HLT 0000
;;; MAIN
;; Print message
ADI _prompt_p
.prompt_loop
JST .print_char
ARD 0000 ; decrement pointer
JST .inc
BNE .prompt_loop
LDA _zero
STA _p_counter
;; Get user input
ADI _inp_p
.inp_loop
RIR _buffer
LDA _buffer
LDT _zero
UFR 0000
BEQ .inp_loop ; Wait for input
LDT _cr
UFR 0000
BEQ .end ; If end of input, do smth else
TAD 0000 ; Otherwise save at pointer
ARD 0000 ; Decrement pointer
LDA _counter ; And count up one
ADA _one
STA _counter
JMP .inp_loop ; Wait for more input
