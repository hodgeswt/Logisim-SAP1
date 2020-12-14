: 0
& ff "Greetings from a long message!"
# e1 00
# e0 01
# df 1e
# de ff
# dd 00
JMP 0e
.print
LBA 00
ATO 00
RST 00
.add
LDA e1
ADA e0
STA e1
LT df
UFR 00
RST 00
.sbb
BTA 00
SBA e0
ATB 00
RST 00
;;; START ;;;
LDB de
.loop
JST .print
JST .sbb
JST .add
BNE .loop
LDA dd
STA e1
HLT 00
