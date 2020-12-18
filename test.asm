: 0
_buffer ffff
_counter fffe
_zero fffd
_one fffc
# _one 1
# fffb fff9
# fffa c
& fff9 "message_one"
# ffee a
ADI fffb
LDA _zero
STA _counter
.a
AIA 0000
ATO 0000
ARD 0000
LDA _counter
ADA _one
STA _counter
LT fffa
UFR 0000
BNE .a
# ffed ffeb
# ffec b
& ffeb "message_two"
ADI ffed
LDA _zero
STA _counter
.b
AIA 0000
ATO 0000
ARD 0000
LDA _counter
ADA _one
STA _counter
LT ffec
UFR 0000
BNE .b
HLT 0000