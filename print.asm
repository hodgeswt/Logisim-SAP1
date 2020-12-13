: 0
& ff "Greetings from an easy-to-use assembler" 
# d7 d8
# d6 ff
# d5 01
LDB d6
LBA 00
ATO 00
BTA 00
SBA d5 ; Subtract 1 from A
LT d7
UFR 00
ATB 00
BNE 01
LBA 00
ATO 00
HLT 00
