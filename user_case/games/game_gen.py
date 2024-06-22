# If you are a VS Code users:
#import sys
#import os
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from puppy.pp.main import Puppy
# from puppy.pp.main import puppy_run

# from puppy.environment.chatting import ChattingHistory
from puppy.llm.open_ai import open_ai_chat

background="""在中世纪的一个小镇上，巫术和神秘力量一直在暗中流传。统治者利用猎巫行动，抓捕了“大巫女”和她的部分信徒，实际上大巫女是小镇最有名的医师，
她发现统治者设下诅咒，使人们容易劳累，健康值不断下降，只能依赖统治者垄断的高价药物。同时统治者在小镇广泛修建诅咒之塔来监管小镇所有的建筑，
受诅咒之塔的影响饿建筑耐久度会变低。统治者因为居民反复修补和建筑建造建筑而获利。玩家作为小镇的外来者，这之前小镇刚刚发生了大规模的猎巫行动，
大量的建筑毁掉，小镇急需再次建设。玩家在游戏中逐渐发现并揭露这个阴谋，解救逃亡的女巫，并与女巫组织合作，瞒过统治者的审查，帮助小镇居民接触诅咒，
让越来越多的人加入自己，恢复小镇的和平与繁荣。

游戏任务目标：游戏共分为三个主要的阶段。
阶段一：玩家没有和女巫组织的人接触，学习统治者的技术建造建筑来建设小镇。
阶段二：接触到女巫组织后，暗中帮助女巫组织，开始学习魔法和女巫建筑，并且秘密帮助其他小镇居民，有越来越多的下级。
阶段三：组织所有人一起反抗统治者，消除诅咒之塔，在小镇周围建起魔法围墙，从独裁中脱离出来。"""

# define the decisiontree for both pp
def game_gen(self, background=background):
    num=0
    while num<5:
        system_prompt=([{"role": "system",
                        "content":
            f"""你是一个游戏的上帝，游戏背景：{background}，现在我们要给玩家设置一个任务，这个任务越离谱越魔幻越好，生成的任务最好和之前的任务有一定程度的设定和事物的关联，但是不要完全相同或者相似。这个任务有一个完成的条件，完成之后用户可以获得奖励，并且引导用户一步一步使得城镇越来越繁荣。
                       ，过去的 task 历史是：{self.task_history},现在用户的资源是：{self.resource}，你只应该处理这些资源，不要新建资源。你的回复应当是 JSON Mode，要标明任务名称，任务的描述，任务完成的条件（达到资源的目标即可,不要生成用户已经达到的资源的任务），和奖励。for example:
                       {{'name': "村子里发洪水了",
                       'description':"发洪水冲坏了村子，你需要收集更多的木头，并且为了稳定民心，你也需要更多的食物"
                       'condition': {{"wood": 100,
                                        "food": 50}}
                       'reward': {{"gold": 100,
                                    "wood": 10}}}}
                       """}])

        response = open_ai_chat(prompt=system_prompt, printing=True, stream=True, temperature=0.9)



        self.task_history.append(response)
        num+=1

# define two threads
holder=Puppy(decisiontree=game_gen)
holder.resource = {"wood": 20, "food": 70, "stone": 50, "gold": 20, "magic":10}
holder.task_history = []

holder.run()
