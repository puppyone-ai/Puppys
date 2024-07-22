# If you are a VS Code users:
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.pp.main import Puppy
from puppy.pp.main import puppy_run



# define the decisiontree for both pp
def chatting_decisiontree(self, system_prompt, max_loop_num=5):

    from user_case.games.four_agent_gotcha_game.chatting import ChattingHistory
    from puppy.llm.open_ai import open_ai_chat
    self.chat_history=ChattingHistory()

    self.chat_history.add(words=system_prompt, role='system')

    loop_num=0
    # repeat the chat for 5 loops
    while loop_num < max_loop_num:

        self.trigger.wait()    # wait for the trigger signal
        print(f"[{self.name}]")
        response = open_ai_chat(prompt=self.chat_history.value, printing=True, stream=True, temperature=0.9)
        self.chat_history.add(words=response, role='assistant')

        # change other_debater's chat_history
        for debater in self.other_debater_list:
            debater.chat_history.add(words=response, role='user')
            debater.trigger.set()

        loop_num += 1

        self.trigger.clear()    # reset self trigger


# define two threads
debater_1=Puppy(name='debater_1', decisiontree=chatting_decisiontree, system_prompt=debater_1_setting)
debater_2=Puppy(name='debater_2', decisiontree=chatting_decisiontree, system_prompt=debater_2_setting)

debater_1.trigger.set()   # set the chatting condition
debater_1.other_debater_list=[debater_2]

debater_2.trigger.clear()
debater_2.other_debater_list=[debater_1]

puppy_run([debater_1, debater_2])
