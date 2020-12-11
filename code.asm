: 0 ; Start at address 0
;
; Set memory addresses ff and fe
# ff ff
# fe ff
; Set output addresses
# fd 01 ; to display if sum == 0
# fc 02 ; to display if sum != 0
;
; Add values and output
LDA ff ; #0
LDB fe ; #1
UFR 00 ; #2
BZO 06 ; #3
; If A + B != 0, do this:
LDA fc ; #4
JMP 07 ; #5
; Else, do this:
LDA fd ; #6
AOT 00 ; #7
HLT 00 ; #8
