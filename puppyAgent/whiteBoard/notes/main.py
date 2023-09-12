# note

class Notes:
    def __init__(self, _noteList:list=[]):
        self.noteList = _noteList

    # noteList should be a list that contains all the notes
    # note is a dictionary
    """
    note = {
        "title": "title",
        "author": "author",
        "discription": "discription",
        "content": "content",
        "time": "time",
        "tag": "tag"
    }
    """

    @property
    def noteList(self):
        return self._noteList
    
    # get the noteList
    def getNoteList(self):
        return self._noteList

    # adding new note
    def addNote(self, newNote:dict):
        self.note.append(newNote)

    # delete note
    def deleteNote(self, noteNum:int):
        self.noteList.pop(noteNum)

    # clear all notes
    def clearNote(self):
        self.noteList = []

    # update note
    def update(self, newNoteList:list):
        self.noteList = newNoteList

    # get the experiment list as a prompt (default mode)
    @property
    def noteListPrompt(self):
        elements = ["title", "author", "discription", "content", "time", "tag"]
        
        prompt = ""
        for i in range(len(self._noteList)):
            prompt += str(i) + ". "
            for elem in elements:
                prompt += self._noteList[i][elem] + "\n"
        return prompt

    # get the experiment list as a prompt (user's mode)
    def getNoteListPrompt(self, elements=None):
        # if user does not specify the elements, then use the default elements
        if elements == None:
            elements = ["title", "author", "discription", "content", "time", "tag"]
        
        prompt = ""
        for i in range(len(self._noteList)):
            prompt += str(i) + ". "
            for elem in elements:
                prompt += self._noteList[i][elem] + "\n"
        return prompt

    

    

    

