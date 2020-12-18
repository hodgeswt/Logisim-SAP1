: 0
_buffer ffff
_counter fffe
_zero fffd
_one fffc
# _one 1
# fffb fff9
# fffa 33
& fff9 "I don't have to manually allocate any more memory."
# ffc7 a
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
# ffc6 ffc4
# ffc5 5
& ffc4 "Ever."
ADI ffc6
LDA _zero
STA _counter
.b
AIA 0000
ATO 0000
ARD 0000
LDA _counter
ADA _one
STA _counter
LT ffc5
UFR 0000
BNE .b
HLT 0000