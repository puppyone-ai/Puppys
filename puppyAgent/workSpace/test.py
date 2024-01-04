def actionFlowTranslate(adjustedSourceCodeList):
    """
    translate the source code to actionFlowJSON and actionFlowPython

    args: sourceCode(Python)
    return: actionFlowHistoryJSON(List), actionFlowHistoryPython(String)
    """
    for actionCode in adjustedSourceCodeList:
        ## return the actionFlowJSON
        lines = actionCode.split('\n')
        searchForDo = False
        comment = ""
        codeSnippet = ""
        actionFlowJSON = []

        for line in lines:
            if '##' in line:
                # if there is an unfinished action, add it to the JSON
                if searchForDo:
                    actionFlowJSON.append({"action": comment, "status": "semi-fixed", "code": actionCode})
                    codeSnippet = ""

                comment = line.split('##', 1)[1].strip()
                searchForDo = True
            else:
                if searchForDo:
                    codeSnippet += line + '\n'  # history code snippet
                    if '.do()' in line:
                        # if there is a .do(), mark it as semi-fixed
                        actionFlowJSON.append({"action": comment, "status": "semi-fixed", "code": actionCode})
                        searchForDo = False
                        codeSnippet = ""
                else:
                    # if not in the comment module, ignore the line
                    pass

        # deal with the last action
        if searchForDo:
            actionFlowJSON.append({"action": comment, "status": "fixed", "code": actionCode})

    return actionFlowJSON, adjustedSourceCodeList

sourceCode = """

nihkdfdsa

## click the button
button = browser.find_element_by_id("button")

"""


sourceCodeList=["## click the button\nbutton = browser.find_element_by_id('button')\npuppy.do()","## click the puppy\nbutton = browser.find_element_by_id('button')"]

JSON,python=actionFlowTranslate(sourceCodeList)
for e in JSON:
    print(e)

for e in python:
    print(e)
    print("\n")
