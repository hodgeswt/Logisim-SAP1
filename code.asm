: 0 ; Start at address 0
;
; Set memory addresses ff and fe
# ff f0
# fe 0f
;
; Add values and output
LDB ff
ADB fe
BOT 00
;
HLT 00
