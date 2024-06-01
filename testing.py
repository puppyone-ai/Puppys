from puppy.pp.main import Puppy

Mei=Puppy()

@Mei
def designing(data_list):

    list=[]
    for data in data_list:

        result=Mei.do(data,action_name="把这组数据处理一下" ,mode= "return")
        list.append(result)

    return list





@Mei
def Hacker_News_Reporter():

    HTML = Mei.do(action_name="Hacker_news的 HTML" , mode= "return")

    news = Mei.do(action_name="Hacker_news的前十条消息", mode="return")

    LLM_related_news= Mei.do(action_name="LLM相关的消息", mode="return")

    return LLM_related_news

