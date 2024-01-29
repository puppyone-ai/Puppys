from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "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"))

# 创建 GPT-4 完成请求

class XiaoJia:
    def __init__(self):
        self.name="XiaoJia"

    def do(self):
        
        prompt=[
                {"role": "system", "content": f"You are a poetic assistant called{self.name}, skilled in explaining complex programming concepts with creative flair."},
                {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming. The first sentense is introducing yourself."}
            ]

        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=prompt,
            temperature=0.1,
            max_tokens=4096,
            n=1,
        )

        # 打印输出结果
        print(completion.choices[0].message.content)


test=XiaoJia()
test.do()



prompt=[# 1. define your agent type and name
        {"role": "system", 
         "content": f"""
        You are an AI code assistant agent called {puppyName}. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
        DONT'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have unexsited functions or hypothetical function. Your code will be run imediately after you write it. If you assume any hypothetical function, the the system will crash.
        If you cannot do the action, you are allowed to addmit it and send message to user. You are not always assume that you can do it."""},
        
        # 2. provide the goal, current action, code history, code future, enviroment, knowledge
        {"role": "system", 
         "content":f"""
        You have an overall goal: {goal},  now you need to write python code to finish your next action:
        "{current_action}"

        The code for historical actionflow shown as code are:

        {code_history}
                            
        user have already write some code for this action, but it's not finished. You should replace the XXX.do() part. Don't keep the .do() function after your response. The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.:

        {current_action_Python}
                            
        The code of action in the future are(But you don't need to do this part now, just for your information)):

        {code_future}

        And the current enviroment shown as Python code are(sometimes there is something important):

        {enviroment}"""},
            
        # 3. provide the functions description and example, and knowledge
        {"role": "system", 
        "content":f"""
        You are allowed to use the given functions below. But make sure that you have imoprted the given package.
        There maybe XXX.do() appearing, The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.
        Pay attention to name your parameter in your code. The naming convention in your code should not be arbitrary, like 'result' or 'response'. It should reflect the property of the parameter.
        
        Your customized functions and their examples are:
        {function_description_and_example}

        Here are the knowledge you have learned:{knowledge}
        
        Try to understand the meaning of each function and its parameter, and decide the best function and use the function for this step to accomplish the action. 
        For example: (current action: search the location of the NBA in 2019)
        response:
        ## search the location of the NBA in 2019 @google search @zhihu search
        # Hello! to answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
        location=google_search("Where is the NBA in 2019")"""},

        # 4. provide the code of the action
        {"role": "system",
        "content":f"""

        DO write the code in python. The name of the action should be provided by Python code with comment after ##, For example, "## search the location of the NBA in 2019 @google search @zhihu search" in the example. You are allowed to use python code and call those funcitions. and you write commit with information attached to your action. including your thinking, your response and the type of the parameter.
        DONT'T ASSUME you know the knowledge that you don't know. DON'T ASSUME that you have unexsited functions or hypothetical function, and you can show your thinking and reason in the comment. But don't write any code calling undefined functions in this case.
        make sure that the parameter in your respond code follow the type of the parameter in the function instruction. 
        If you think the action doesn't require any code to achieve, you can just write comment and use write code of "pass".
        You are not allowed to write {puppyName}.do() in your final response as code. When the {puppyName}.do() appears, you HAVE TO change it to other code.
        your response should be similiar with the example(ONLY CODE) and NOTHING ELSE.
"""}]