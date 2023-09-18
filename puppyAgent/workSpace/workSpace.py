import threading

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

    #get the list of agent
    def getPuppy(self):
        return self.puppyList
    
    #get the list of human
    def getHuman(self):
        return self.humanList

    #add a agent
    def addPuppy(self, puppyName, puppyDiscription, puppyAuthoritiedTools, puppyMessageBox, puppyLocalNotes):
        if puppyName not in self.puppyList:
            self.puppyList[puppyName] = {"name": puppyName, "discription": puppyDiscription, "authoritiedTools": puppyAuthoritiedTools, "messageBox": puppyMessageBox, "localNotes": puppyLocalNotes}
        else:
            self.puppyList[puppyName]['name'] = puppyName
            self.puppyList[puppyName]['discription'] = puppyDiscription
            self.puppyList[puppyName]['authoritiedTools'] = puppyAuthoritiedTools
            self.puppyList[puppyName]['messageBox'] = puppyMessageBox
            self.puppyList[puppyName]['localNotes'] = puppyLocalNotes

    #remove a agent
    def removePuppy(self, puppyName):
        if puppyName in self.puppyList:
            del self.puppyList[puppyName]

    #add a human
    def addHuman(self, humanName, humanDiscription):
        if humanName not in self.humanList:
            self.humanList[humanName] = {"name": humanName, "discription": humanDiscription}
        else:
            self.humanList[humanName]['name'] = humanName
            self.humanList[humanName]['discription'] = humanDiscription
    
    #remove a human
    def removeHuman(self, humanName):
        if humanName in self.humanList:
            del self.humanList[humanName]

    #run a single agent
    def runAgent(self, agentName):
        print(f"Thread for agent: {agentName} is running")

        # to be continued
        pass

    #run all agents
    def run(self):
        threads = []

        for agentName in self.puppyList:
            t = threading.Thread(target=self.runAgent, args=(agentName,))
            threads.append(t)
            t.start()

        # wait for all threads to finish
        for t in threads:
            t.join()
        
        print("All threads finished.")
        

if __name__=="__main__":
    workSpace = workSpace()
    workSpace.addPuppy("David", "an leader agent", ["tool1", "tool2"], ["message1", "message2"], ["note1", "note2"])
    workSpace.addPuppy("Alice", "a COO", ["tool1", "tool2"], ["message1", "message2"], ["note1", "note2"])
    workSpace.run()