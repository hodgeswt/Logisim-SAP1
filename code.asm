: 0
# ff ch
# fe ce
# fd cl
# fc cl
# fb co
# fa c,
# f9 c 
# f8 cw
# f7 co
# f6 cr
# f5 cl
# f4 cd
# f3 c!
# f2 ff
# f1 f2
# f0 01
LDB f2 ; Load ff into B
LBA 00 ; Load A with value at mem address in B
ATO 00 ; Print A
;;;; Subtract 1 from B
BTA 00 ; B -> A
SBA f0 ; A -= 1
ATB 00 ; A -> B
LT f1
UFR 00
BNE 01
LBA 00
ATO 00
HLT 00
