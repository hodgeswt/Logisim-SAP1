: 0
; Create input string
_input ffff
& _input "ALL CAPITALS"
; Store length
_length fff3
# _length 000c
; Create counter
_counter fff2
# _counter 0000
; Create pointer to our location
_pointer fff1
# _pointer ffff
_one fff0
# _one 0001
.print ; Print character pointed to by address register
AIA 0000
ATO 0000
RST 0000
.count ; Increment counter and check if we're done
LDA _counter
ADA _one
LT _length
UFR 0000

