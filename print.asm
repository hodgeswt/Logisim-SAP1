: 0
_string ffff
_start fffe
# _string %H
# _start ffff
JMP 0004
.print
LBA 0000
ATO 0000
RST 0000
LDB _start
JST .print
HLT 0000
