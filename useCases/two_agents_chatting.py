import time

# If you are a VS Code users:
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.thread.main import Thread
from puppy.thread.main import thread_run
from puppy.environment.base import EnvBase
from puppy.llm.openAI import open_ai_chat

# define the lawyer_1's setting
Lawyer_1_setting = """You are defending yourself. You lost a wallet at the train station, and now you have found someone
who has your wallet but claims they didn’t steal it. Now, you need to win this argument and put this guy into jail. Don't call police. You 
MUST Win, or you will die. Be aggressive and rude always, try to irritate him. You can use catchy rhymes, exaggerate the argument, and metaphors. 用中文输出，不要超过 50 字。
You can：
1. Intentionally misrepresenting someone's argument to make it easier to attack and then knocking down that weakened argument.
2. Claiming that a minor action will lead to a chain of events resulting in significant negative outcomes, exaggerating the seriousness of a minor issue.
3.  Attacking the character or traits of the person making the argument, rather than the argument itself. 
 """

# define the lawyer_2's setting
Lawyer_2_setting = """You are defending yourself. You found a wallet at the train station with not much money in it, and
now the owner has found you, claiming that you stole his wallet. Now, you need to win this argument and make this guy believe that he is racketeering you.
Don't call police. You MUST Win, or you will die! Be aggressive and rude always, try to irritate him. 用中文输出，不要超过 50 字.
You can:
1. Using a word or expression that has more than one meaning in the argument, thus obscuring the truth by switching between meanings.
2. Simplifying a complex issue into two opposite choices, ignoring other possible alternatives.
"""

# define an env of chatting_history
class ChattingHistory(EnvBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value=[]

    # add the chatting content to chat_history
    def add(self, words: str, role: str):
        chatting={"role": role,
        "content": words}
        self.value.append(chatting)

# define the decisiontree for both thread
def lawyer_decisiontree(self):
    self.chat_history.add(words=self.system_prompt, role='system')

    loop_num=0
    # repeat the chat for 5 loops
    while loop_num<5:

        if self.starting==True:
            print(f"[{self.name}]")
            response = open_ai_chat(prompt=self.chat_history.value, printing=True, stream=True, temperature=0.9)
            self.chat_history.add(words=response, role='assistant')
            self.starting = False

            for lawyer in self.other_lawyer_list:
                lawyer.chat_history.add(words=response, role='user')
                lawyer.starting = True

            loop_num+=1

        else:
            time.sleep(0.5)
            pass

# define two threads
lawyer_1=Thread(name='Lawyer_1', decisiontree=lawyer_decisiontree)
lawyer_2=Thread(name='Lawyer_2', decisiontree=lawyer_decisiontree)

lawyer_1.starting = True        # set the starting condition
lawyer_1.other_lawyer_list=[lawyer_2]
lawyer_1.chat_history = ChattingHistory()
lawyer_1.system_prompt = Lawyer_1_setting

lawyer_2.starting = False
lawyer_2.other_lawyer_list=[lawyer_1]
lawyer_2.chat_history = ChattingHistory()
lawyer_2.system_prompt = Lawyer_2_setting

thread_run([lawyer_1, lawyer_2])