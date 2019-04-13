import print_color as pc

print(pc.CBOLD,     "CBOLD     ", pc.CEND, pc.CRED,    "CRED   ", pc.CRED2,    "CRED2",    pc.CEND)
print(pc.CITALIC,   "CITALIC   ", pc.CEND, pc.CGREEN,  "CGREEN ", pc.CGREEN2,  "CGREEN2",  pc.CEND)
print(pc.CURL,      "CURL      ", pc.CEND, pc.CYELLOW, "CYELLOW", pc.CYELLOW2, "CYELLOW2", pc.CEND)
print(pc.CBLINK,    "CBLINK    ", pc.CEND, pc.CBLUE,   "CBLUE  ", pc.CBLUE2,   "CBLUE2",   pc.CEND)
print(pc.CBLINK2,   "CBLINK2   ", pc.CEND, pc.CVIOLET, "CVIOLET", pc.CVIOLET2, "CVIOLET2", pc.CEND)
print(pc.CSELECTED, "CSELECTED ", pc.CEND, pc.CBEIGE,  "CBEIGE ", pc.CBEIGE2,  "CBEIGE2",  pc.CEND)
print(pc.CGREY,     "CGREY     ", pc.CEND, pc.CWHITE,  "CWHITE ", pc.CWHITE2,  "CWHITE2",  pc.CEND)

print(pc.CBLACK + pc.CWHITEBG,  "CBLACK + CWHITEBG  ", pc.CEND)
print(pc.CWHITE + pc.CGREYBG,   "CWHITE + CGREYBG   ", pc.CEND)
print(pc.CWHITE + pc.CBLACKBG,  "CWHITE + CBLACKBG  ", pc.CEND)
print(pc.CBLACK + pc.CREDBG,    "CBLACK + CREDBG    ", pc.CBLACK  + pc.CREDBG2,    "CBLACK  + CREDBG2    ",pc.CEND)
print(pc.CBLACK + pc.CGREENBG,  "CBLACK + CGREENBG  ", pc.CBLACK  + pc.CGREENBG2,  "CBLACK  + CGREENBG2  ",pc.CEND)
print(pc.CBLACK + pc.CYELLOWBG, "CBLACK + CYELLOWBG ", pc.CBLACK  + pc.CYELLOWBG2, "CBLACK  + CYELLOWBG2 ",pc.CEND)
print(pc.CWHITE + pc.CBLUEBG,   "CWHITE + CBLUEBG   ", pc.CWHITE2 + pc.CBLUEBG2,   "CWHITE2 + CBLUEBG2   ",pc.CEND)
print(pc.CWHITE + pc.CVIOLETBG, "CWHITE + CVIOLETBG ", pc.CWHITE2 + pc.CVIOLETBG2, "CWHITE2 + CVIOLETBG2 ",pc.CEND)
print(pc.CBLACK + pc.CBEIGEBG,  "CBLACK + CBEIGEBG  ", pc.CBLACK  + pc.CBEIGEBG2,  "CBLACK  + CBEIGEBG2  ",pc.CEND)
