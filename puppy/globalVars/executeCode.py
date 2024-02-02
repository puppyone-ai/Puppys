

globalVars =globals()

def executeCodeTracked(trackCode,globals=globalVars):
    print("Global!!!!!!!!!!!!!")
    #print(globalVars)
    exec(trackCode)
    

def executeCodeHidden(hiddenCode,globals=globalVars):
    exec(hiddenCode)