: 0 ; Start at address 0
;
; Set memory addresses ff and fe
# ff f0
# fe 0f
; Set fd and fc
# fd 00
# fc 01
;
; Add values and output
LDA ff
LDB fe
UFR 00
BEQ 06
; If A and B are not equal, do this:
LDA fd
JMP 07
; Else, do this:
LDA fc
AOT 00
HLT 00
