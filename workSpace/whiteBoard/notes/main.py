# note

class Notes:
    def __init__(self, _noteList:list=[]):
        self.noteList = _noteList

    # noteList should be a list that contains all the notes
    # note is a dictionary
    """
    note = {
        "title": "title",
        "discription": "discription",
        "author": "author",
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

    

    

    

    

