: 0
_a ffff
# _a 42
_b fffe
# _b ff
JMP 06
.bot
PHA 00
LDA _b
AOT 00
PLA 00
RST 00
;;; MAIN
LDA _a
JST .bot
AOT 00
HLT 00
