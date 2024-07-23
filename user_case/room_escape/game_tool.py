class Tool:
    def __init__(self, name, description, use_guide, useful, actions=None, subtools=None):
        """
        Initialize a tool with its properties.
        Args:
            name (str): Name of the tool.
            description (str): Description of the tool.
            use_guide (str): Guide on how to use the tool.
            useful (bool): Whether the tool is useful for escaping.
            actions (dict): Actions possible with this tool and their outcomes.
            subtools (list): List of sub-tools contained within this tool.
        """
        self.name = name
        self.description = description
        self.use_guide = use_guide
        self.useful = useful
        self.actions = actions if actions else {}
        self.subtools = subtools if subtools else []
        self.taken = False
        self.used = 0

    def add_subtool(self, subtool):
        """
        Add a subtool to this tool.
        Args:
            subtool (Tool): The subtool to add.
        """
        self.subtools.append(subtool)

    def display(self):
        """
        Display tool information and its subtools when the agent encounters it.
        """
        info = f"{self.name} - {self.description}\nUse: {self.use_guide}"
        for subtool in self.subtools:
            info += f"\nSubtool: {subtool.display()}"
        return info

    def take_tool(self):
        """ Mark this tool as taken. """
        self.taken = True

    def use_tool(self):
        """ Increase the use count of this tool by 1. """
        self.used += 1

    def add_action(self, action_name, action_result):
        """
        Add an action and its result to the tool.
        Args:
            action_name (str): The name of the action.
            action_result (str): The result or description of performing the action.
        """
        self.actions[action_name] = action_result
