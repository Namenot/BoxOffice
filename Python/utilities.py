
def checkspaces(a):
    nos = 30 #number of spaces
    nos -= len(a)
    if nos >=0:
        strg = a
        for a in range(nos+5):
            strg += " "
    else:
        strg = a[:nos]
        strg += "...  "
    return strg
