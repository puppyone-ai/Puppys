from collections import deque

class Actions:
    def __init__(self, source_code: str = "", llm: str = 'gpt', **kwargs):

        self.actions_list = deque()
        self.llm = llm

        if "thread_instance" in kwargs:
            thread_instance = kwargs["thread_instance"]
            self.thread_instance = thread_instance

        self._parse_func_code_into_actions(source_code)
        self._check_status()

        """
        ActionList: [action,action,action]

        [
        {"name": "", "code": "Mei.do()", "status": "changeable"，“llm”: "gpt"},
        {"name": "", "code": "",         "status": "",           “llm”:      }
        ]
        """

        # could consider introduce the func_name indexing in the future

    #TODO: abstract the parser to convert the source code to diverse properties

    def _parse_func_code_into_actions(self, source_code: str) -> None:

        """
        Load the action from source code so that we could trigger it in actionflow
        """

        # clean source code

        lines = source_code.split('\n')

        striped_lines = []

        for line in lines[2:]:  # [2:]filter decorator and function name
            line = line.strip()
            if line:
                striped_lines.append(line)

        # print('striped_lines:')
        # print(striped_lines)

        # load source code to action list sequentially

        for line in striped_lines:

            if '##' in line:
                self.actions_list.append({"name": "",
                                         "code": "",
                                          "status": "",
                                          "llm": self.llm})

                self.actions_list[-1]["name"] = line.split('##', 1)[1].strip()
                self.actions_list[-1]["code"] += f'{line}\n'

            else:

                self.actions_list[-1]["code"] += line + '\n'

    # verify the status of the action
    def _check_status(self) -> None:

        for action in self.actions_list:

                if ".do()" in action["code"]:

                    if not action["name"]:
                        action["status"] = "changeable"
                    else:
                        action["status"] = "semi-fixed"

                else:
                    action["status"] = "fixed"
