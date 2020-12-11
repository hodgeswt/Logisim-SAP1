: 0 ; Start at address 0
;
; Set memory addresses ff and fe
# ff f0
# fe ff
# fd 0f
LDA ff ; #0
LDB fe ; #1
PHB 00 ; #2
ADA fd ; #3
PLB 00 ; #4
BOT 00 ; #5
HLT 00 ; #6
