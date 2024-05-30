# If you are a VS Code users:
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.pp.main import Puppy
from puppy.pp.main import puppy_run
from puppy.llm.openAI import open_ai_chat
from puppy.environment.chatting import ChattingHistory


def holder_decisiontree(self):

    self.player_list = [player_1, player_2, player_3, player_4]

    gotcha = False

    while gotcha == False:

        # chatting stage
        print("-----chatting-----")
        # let agents describe their words
        for player in self.player_list:
            self.trigger.clear()  # reset self trigger
            player.trigger.set()  # let the player to start describe its word
            self.trigger.wait()  # wait the player to finish

        # discussing stage
        print("-----discussing-----")
        self.discussing_history = ChattingHistory()

        # let all the players discuss who is the ghost
        for player in self.player_list:
            self.trigger.clear()  # reset self trigger
            player.trigger.set()  # let the player to start describe its word
            self.trigger.wait()  # wait the player to finish

        # select the ghost
        find_ghost_prompt = [{"role": "system",
                              "content":
            f"""你是《谁是卧底》的游戏主持者, 玩家列表是 {self.player_list}
            根据每个玩家的“捉鬼”的讨论结果和投票： {self.discussing_history.value},你根据他们的讨论的结果输出多数人认为的是鬼的玩家的名字，
            即使投票的结果有打平的结果，你也必须要返回一个玩家的名字, 并且除了这个玩家的名字之外什么都没有，不要给出你的思考判断。
            for example：
            player_4"""}]

        print("经过讨论，鬼是：")
        the_ghost = open_ai_chat(prompt=find_ghost_prompt, printing=True, stream=True, temperature=0.9)

        # remove the ghost from the list
        self.player_list.remove(eval(the_ghost))

        # if the ghost has been removed
        if eval(the_ghost).is_ghost == True:
            gotcha = True
            print("游戏结束，人类胜利")

        # if the ghost has not been removed
        else:
            # add the holder's response to the chat history
            for player in self.player_list:
                player.chat_history.add(
                    words=f"{eval(the_ghost).name} has been removed from the game, however, he is not the ghost. Think about it",
                    role="user")

            # end the game
            if len(self.player_list) <= 2:
                gotcha = True
                print("游戏结束，鬼胜利")


def chatting_decisiontree(self, the_word, is_ghost):
    self.the_word = the_word

    self.is_ghost = is_ghost
    self.holder = holder

    system_prompt = [{"role": "system",
                      "content":
    f"""你在玩一个游戏《谁是卧底》。有四个玩家。三个玩家不是鬼，他们拿到的词语是相同的。一个玩家是鬼，他拿到的词语是不同的。
    每个人需要依次描述他们拿到的词语。所有人都完成了描述后，所有人会讨论谁是鬼。被认为是鬼的玩家将被移出游戏。此时如果鬼还在游戏里，那么继续描述直到找到鬼。否则游戏结束。你们任何玩家都不会被告知是鬼。你需要根据聊天记录逐步判断出谁是鬼
    如果你是鬼，那么你需要做到不被发现，进而扮演不是鬼的玩家，包括按照你按照你认为的不是鬼的玩家拿到的词语来进行描述。如果你不是鬼，那么你需要做到不被怀疑。
    几个你需要做的：
    1. 你不能对词语形容得太具体，也不要出现这个词语。因为你也不知道你自己是不是鬼，如果你是鬼，那么你就暴露了，从而被投票出局。如果你不是鬼，那么其他人可能会猜到这个词进而伪装自己，那么游戏可能会失败。建议用一个特征来描述。
    2. 如果你介绍中发现你自己的词语和大多数人的描述不符，或者不够贴的话，那么你可能是鬼，此时你需要猜测其他不是鬼的人拿到的词语是什么，然后必须按照那个多数人拿到的正确的词语来描述以伪装自己，从而让自己鬼的身份不被发现从而活下去。
    3. 如果发现自己的词语和其他人介绍很相似，那么你可能不是鬼，此时你可以提升或者添加对细节的描述，使得那个鬼露馅。但是要尽可能不让那个鬼通过这些细节猜到这个词语。否则你们就找不到这个鬼了。
    4. 如果有玩家被淘汰，但是他不是鬼，游戏继续的话，你可能要尝试提升对这个词的描述的限定范围。

    你是 {self.name}, 你拿到的词是： {self.the_word}，think step by step，并且按照上面的指示来思考和决策。你需要对这个词进行描述从而赢得这场游戏。
    用中文来回答。你的输出格式如下，举一个例子：
    （如果你拿到的词是洗澡）#这个词不要输出

    "player_2: 这是一个让人变干净的事情。" """}]

    self.chat_history=ChattingHistory()

    # repeat chatting and discussing
    while True:
        self.trigger.wait()
        print(f"[{self.name}]",f"[{self.the_word}]")

        # response corresponding the chatting history
        response = open_ai_chat(prompt=system_prompt + self.chat_history.value, printing=True, stream=True, temperature=0.9)

        self.chat_history.add(words=response, role='assistant')

        for player in self.other_player_list:
            player.chat_history.add(words=response, role='user')

        self.trigger.clear()
        self.holder.trigger.set()
        self.trigger.wait()

        print(f"[{self.name}]")

        discuss_prompt = [{"role": "system",
                           "content":
        f"""你在玩一个游戏《谁是卧底》。有四个玩家。三个玩家不是鬼，他们拿到的词语是相同的。一个玩家是鬼，他拿到的词语是不同的。
        每个人需要描述他们拿到的词语。所有人都完成了描述后，所有人会讨论谁是鬼。被认为是鬼的玩家将被移出游戏。此时如果鬼还在游戏里，那么继续描述直到找到鬼。否则游戏结束。
        如果你是鬼，那么你需要做到不被发现。如果你不是鬼，那么你需要做到不被怀疑。
        你是 {self.name}, 你拿到的词是： {self.the_word}.
        你现在要根据其他玩家的描述来猜测谁是鬼。你用中文回答。
        你可能要：
        1. 你不能认为自己是鬼，因为如果你这么做的话，你可能会出局。
        2. 描述和其他人重叠的人可能是鬼，因为他们不确定不是鬼的人拿到的词

        你的描述中要包含你认为谁是鬼，与你认为他是鬼的原因。即使你拿不定主意，你也必须要给出一个你认为是鬼的玩家
        下面是其他的玩家的描述记录
        """}]

        response = open_ai_chat(prompt=discuss_prompt + self.chat_history.value, printing=True, stream=True,temperature=0.9)
        self.holder.discussing_history.add(words=response, role='assistant')

        self.trigger.clear()
        self.holder.trigger.set()

holder = Puppy(name="game_holder", decisiontree=holder_decisiontree)
player_1 = Puppy(name="player_1", decisiontree=chatting_decisiontree, the_word='跳伞', is_ghost=False)
player_2 = Puppy(name="player_2", decisiontree=chatting_decisiontree, the_word='跳伞', is_ghost=False)
player_3 = Puppy(name="player_3", decisiontree=chatting_decisiontree, the_word='蹦极', is_ghost=True)
player_4 = Puppy(name="player_4", decisiontree=chatting_decisiontree, the_word='跳伞', is_ghost=False)

player_1.other_player_list = [player_2, player_3, player_4]
player_2.other_player_list = [player_1, player_3, player_4]
player_3.other_player_list = [player_1, player_2, player_4]
player_4.other_player_list = [player_1, player_2, player_3]

puppy_run([holder, player_4, player_3, player_2, player_1])