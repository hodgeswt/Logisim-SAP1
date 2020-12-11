: 0 ; Start at address 0
;
; Set memory addresses ff and fe
# ff f0
# fe ff
# fd 0f
LDA ff ; #0
LDB fe ; #1
ADA fd ; #2
BOT 00 ; #3
HLT 00 ; #4
