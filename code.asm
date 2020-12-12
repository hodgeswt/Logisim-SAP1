: 0 ; Start at address 0
;
; Set memory values
# ff 20
# fd 20
# fc ff
LDB ff
LDA fc
PHA 00
BTA 00
ADA fd
ATB 00
PLA 00
AOT 00
LDC fd
COT 00
NOP 00
BOT 00
HLT 00
