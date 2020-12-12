: 0 ; Start at address 0
;
; Set memory values
# ff 42
# fd 02
# fc 08
JMP 09
PHA 00
LDA 00
ADA fd
LT fc
BNE 03
ATB 00
PLA 00
RST 01
LDA ff
JST 01
AOT 00 ; PRINT 42
NOP 00
NOP 00
BOT 00 ; PRINT 08
HLT 00
