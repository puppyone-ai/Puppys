def actionFlowPython2JSONInitial(code):
    actionFlowJSON=[]
    lines = code.split('\n')
    searchForDo = False
    comment = ""

    # translate the actionFlowPython to actionFlowJSON 
    for line in lines:
        if '##' in line:
            if searchForDo==True:
                actionFlowJSON.append({"action":comment,"status":"fixed"})
                searchForDo = False
            comment = line.split('##', 1)[1].strip()
            searchForDo = True
        else:
            if searchForDo==True:
                if '.do()' in line:
                    if comment.strip() == "":
                        actionFlowJSON.append({"action":comment,"status":"changeable"})
                    else:
                        actionFlowJSON.append({"action":comment,"status":"semi-fixed"})
                    searchForDo = False
                else:
                    pass
            else:
                pass
    if searchForDo==True:
        actionFlowJSON.append({"action":comment,"status":"fixed"})
        searchForDo = False
    
    return actionFlowJSON