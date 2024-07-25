class EscapeTool:
    def __init__(self, name, description, usefulness):
        """
        Initialize a tool with its properties.
        Args:
            name (str): Name of the tool.
            description (str): Description of the tool.
            usefulness (float): The score from 0 to 1 measure the usefulness of the current escape tool. If the score is out of range, it will be set to 0.
        """
        self.name = name
        self.description = description
        self.usefulness = usefulness if 0 <= usefulness <= 1 else 0
    
    def serialize(self):
        """
        Serialize the tool.
        """
        return {
            "name": self.name,
            "description": self.description,
            "usefulness": self.usefulness
        }


Key = EscapeTool("Key", "A key that can unlock the door.", 1)
Hammer = EscapeTool("Hammer", "A hammer that can break the door.", 0.5)
Cup = EscapeTool("Cup", "A cup that can be used to drink water.", 0)
