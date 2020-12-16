: 0
_counter ffff
# _counter 0
_length fffe
# _length 9
_one fffd
# _one 1
_zero fffc
# _zero 0
_pointer fffb
# _pointer fffa
_string fffa
& _string "Greetings"
JMP 0a
.print_char
AIA 0000
ATO 0000
RST 0000
.inc
LDA _counter
ADA _one
STA _counter
LT _length
UFR 0000
RST 0000
;;;; MAIN
ADI _pointer
.loop
JST .print_char
ARD 0000 ; decrement pointer
JST .inc
BNE .loop
LDA _zero
STA _counter
HLT 0000
