class workSpace:
    def __init__(self, puppyList:dict={}, human:dict={}): # puppy, human, whiteBoard, toolsBox
        
        self.puppyList = puppyList #dictionary puppy
        {"David":{
            "name": "David",
            "discription": "an leader agent",            
            "authoritiedTools":["tool1", "tool2"], 
            "messageBox": ["message1", "message2"],
            "localNotes": ["note1", "note2"],
        },
        "Jacob":{
            "name": "Jacob",
            "discription": "an leader agent",
            "authoritiedTools":["tool1", "tool2"], 
            "messageBox": ["message1", "message2"],
            "localNotes": ["note1", "note2"],
        },
        }

        
        self.humanList = human #unkown
        {"Jack":{
            "name": "Jack",
            "discription": "The final boss of every agent"
        }}


    def getPuppy(self):
        return self.puppyList
    
    def getHuman(self):
        return self.humanList

    def addPuppy(self, puppyName, puppyDiscription, puppyAuthoritiedTools, puppyMessageBox, puppyLocalNotes):
        if puppyName not in self.puppyList:
            self.puppyList[puppyName] = {"name": puppyName, "discription": puppyDiscription, "authoritiedTools": puppyAuthoritiedTools, "messageBox": puppyMessageBox, "localNotes": puppyLocalNotes}
        else:
            self.puppyList[puppyName]['name'] = puppyName
            self.puppyList[puppyName]['discription'] = puppyDiscription
            self.puppyList[puppyName]['authoritiedTools'] = puppyAuthoritiedTools
            self.puppyList[puppyName]['messageBox'] = puppyMessageBox
            self.puppyList[puppyName]['localNotes'] = puppyLocalNotes

    def removePuppy(self, puppyName):
        if puppyName in self.puppyList:
            del self.puppyList[puppyName]

    def addHuman(self, humanName, humanDiscription):
        if humanName not in self.humanList:
            self.humanList[humanName] = {"name": humanName, "discription": humanDiscription}
        else:
            self.humanList[humanName]['name'] = humanName
            self.humanList[humanName]['discription'] = humanDiscription
    
    def removeHuman(self, humanName):
        if humanName in self.humanList:
            del self.humanList[humanName]



    


    
    




