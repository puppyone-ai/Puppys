import os
from puppy.llm.openAI import open_ai_chat
from puppy.thread.actionflow.action import Action


# provide the goal, current action, code history, code future, environment, knowledge
def sense(thread_instance) -> str:

    return f"""
    You have an overall long-term goal: {thread_instance.goal},  and your current action is:
    {thread_instance.attention.name}

    The code for historical actionflow shown as code are:
    {thread_instance.actionflow.get_code(history=True)}

    The code of action in the future are(But you don't need to do this part now, just for your information)):
    {thread_instance.actionflow.get_code(pending=True, current=True)}"""


def check(thread_instance, action, show_prompt=False) -> None:

    """
    check the action and write corresponding code
    """

    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content": f"""
    You are an AI code assistant agent called {thread_instance.puppy_name}. 
    1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
    2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately after you write it. If you assume any hypothetical function, the system will crash.
    3. You need to justify if your current action has been achieved or not by history code, and decide to skip the current action or not.
    4. You only need to decide if your current action has been achieved or not. You don't need to write code to achieve it."""},

        # 2. set the standard of if the action is done or not
        {"role": "system",
         "content": f"""
    You justify if your current action is done or not, you have two choices:
    1. Done: That means you don't need to write code to achieve it again. The action history shows that you have already know what you want to know or have already achieve the action. In this case, you should write Python code to return Ture, and your generated code should be:
    finishedOrNot=True

    2. Unfinished: That means you need to write code to achieve it again, or there are some unfinished actions that you need to make . In this case, you should write Python code to return False, and the your generated code should be:
    finishedOrNot=False

    for example:
    1. the latest action in the action history: 
    ## 发信息给我妈妈 @ask for help
    # Since I don't have any information about the user's mother or the content of the message, I need to ask the user for help.
    message_content = XiaoMei.askHumanForHelp.run("What message would you like to send to your mom?")
    # the user claimed that the message is "I love you mom"

    your response:
    # the action is not done, because I get what I should send, but I haven't send it yet. Maybe next action is to send it
    finishedOrNot=False

    2. current action:
    ## get what happened about COVID in the the 2nd Feb 2020 @google search
    # I need to search the information about what happened in the the 2nd Feb 2020. The function returns as a string.
    result=google_search("What happened in the the 2nd Feb 2020")
    # the result is "First death resulting from Coronavirus outside China reported."

    your response:
    # I get what I should get, and I don't need to do anything else if there is no other action provide by human.
    finishedOrNot=True"""},

        # 3. provide the goal, current action, code history, code future, environment, knowledge
        {"role": "system",
         "content": f"""
    {sense(thread_instance)}"""},

        # 4. justify if the action is done or not
        {"role": "user",
         "content": f"""
    Now you need to write code to justify if the action is done or not: \n{action.code}
    Your answer is:
    """}
    ]

    if show_prompt:
        print("\t*******checking prompt********")
        for chunk in prompt:
            print(chunk['content'])

    print("\n\U00002705 Checking Code ##############################################################")

    new_code = open_ai_chat(prompt=prompt,
                            model="gpt-4-turbo",
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=True, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    # deliver 'finishedOrNot' to the environment for verification of the final execution.
    exec(new_code, thread_instance.exec_environment)


def achieve(thread_instance, action, show_prompt=False) -> Action:

    """
    write code to achieve the action
    """

    # prompt for actionDo **************************************************************************************
    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content": f"""
    You are an AI code assistant agent called {thread_instance.puppy_name}. 
    1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code. for example: # Hello, I am an assistant.
    2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately after you write it. If you assume any hypothetical function, the the system will crash.
    3. If you cannot do the action, you are allowed to send message to user for help.
    4. Your response cannot only be comment. You HAVE to write codes"""},

        # 2. provide the functions description and example, and knowledge
        {"role": "system",
         "content": f"""
    You are allowed to use the given functions below. But make sure that you have imported the given package.
    There maybe XXX.do() appearing, The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.
    Pay attention to name your parameter in your code. The naming convention in your code should not be arbitrary, like 'result' or 'response'. It should reflect the property of the parameter.

    Your customized functions and their examples are:
    {thread_instance.tool_box.tools_dict}

    Try to understand the meaning of each function and its parameter, and decide the best function and use the function for this step to accomplish the action. 
    For example: (current action: search the location of the NBA in 2019@ google search @zhihu search)
    response:
    # Hello! to answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
    location=google_search("Where is the NBA in 2019"
    location= zhihu_search("Where is the NBA in 2019")"""},

        # 3. provide the goal, current action, code history, code future, environment, knowledge

        {"role": "system",
         "content": f"""
    {sense(thread_instance)}"""},

        # 4. provide the code of the action
        {"role": "user",
         "content": f"""
    user have already write some code for this action, but it's not finished. You should replace the XXX.do() part. Don't keep the .do() function after your response. The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.:
    \n{action.code}
    Now you write code to achieve your action: {action.name}
    DON'T ASSUME you know the knowledge that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function, and you can show your thinking and reason in the comment. But don't write any code calling undefined functions in this case.
    make sure that the parameter in your respond code follow the type of the parameter in the function instruction. .
    You are NOT allowed to write {thread_instance.puppy_name}.do() in your final response as code. When the {thread_instance.puppy_name}.do() appears, you HAVE TO change it to other code.
    your response should be similar with the example(ONLY CODE) and NOTHING ELSE.
    """}]

    # prompt finished *****************************************************************************************

    print("\n\U0001F697 Running Code ################################################################")

    if show_prompt:
        print("\t*******planning prompt********")
        for chunk in prompt:
            print(chunk['content'])

    new_code = open_ai_chat(prompt=prompt,
                            model="gpt-4-turbo",
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=True, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    action = Action()
    action.name = action.name
    action.code = new_code
    action.status = "fixed"

    return action
