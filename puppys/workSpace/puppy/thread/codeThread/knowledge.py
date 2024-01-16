class Knowledge():
    def __init__(self, codeThreadInstance):
        self.codeThreadInstance = codeThreadInstance
        self.knowledge = []

    def getKnowledge(self):
        return self.knowledge
    
    def getKnowledgeStr(self):
        knowledgeStr=""
        for knowledge in self.knowledge:
            knowledgeStr=knowledgeStr+knowledge+"\n"
        return knowledgeStr
    
    def addKnowledge(self,knowledge):   
        self.knowledge.append(knowledge)

    def clearKnowledge(self):
        self.knowledge = []
