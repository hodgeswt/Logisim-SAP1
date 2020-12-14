: 0
& ff "UwU"
# fc 01
# fb ff
# fa 03
# f9 00
JMP 08
.print
LBA 00
ATO 00
RST 00
.sbb
BTA 00
SBA fc ; A -= 1
ATB 00
RST 00
;; MAIN
LDB fb
.loop
JST .print
JST .sbb
LDA f9
ADA fc
STA f9
LT fa
UFR 00
BNE .loop
HLT 00
