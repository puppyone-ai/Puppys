import os
from puppy.llm.openAI import open_ai_chat
from puppy.thread.actionflow.action import Action
from puppy.thread.base import ThreadBase


def plan_next_action(thread_instance: ThreadBase, action: Action, show_prompt: bool = False) -> Action:

    """
    let the agent conceive some thoughts to define the action so that it could be achieved.
    """

    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content": f"""
        You are an AI code assistant agent. All the plan must be executable Python code.
        You always plan with natural language output, for example: Hello, I am an assistant.
        If you cannot understand the goal, you are allowed to send message to user for help.
        """},


        # 2. provide the example
        {"role": "system",
         "content": """
        For example:
        
        {
        "goal": "prepare a meal",
        
        "historical action":"
        ## Decide what to have for dinner and list the needed ingredients.
        menu = "Spaghetti Carbonate"
        ingredients = ["spaghetti", "bacon", "eggs", "parmesan cheese"]"
        
        "YOUR RESPONSE":"
        ## Buy the ingredients and then wash, cut, and prepare them.
        print("Buying ingredients:", ingredients)
        print("Washing and cutting ingredients.")
        "
        
        "The action in the future":"
        ## Cook the prepared ingredients according to the recipe, and then serve the meal.
        print("Cooking", prepared_ingredients)
        print("Dinner is ready and served!")"
        }
        
        YOUR RESPONSE:
        Buy the ingredients and then wash, cut, and prepare them.
        """},

        # 3. provide the goal, current action, code history, code future, environment, knowledge
        {"role": "system",
         "content": f"""
        You have an overall long-term goal: {thread_instance.goal},  and your current action is:
        {thread_instance.action_tracked.name}
        
        The code for historical actionflow shown as code are:
        {thread_instance.actionflow.get_code(history=True)}
        
        The code of action in the future are(But you don't need to do this part now, just for your information)):
        {thread_instance.actionflow.get_code(pending=True, current=True)}

        your formally-defined parameters and their previewing are as follows: 
        {thread_instance.exec_environment.preview()}"""},


        # 4. conceive the action
        {"role": "user",
         "content": f"""
        your text should be similar with the example(ONLY TEXT) and NOTHING ELSE.
        Now you write text to plan your next action,don't write any code in this case.

        response:
        """}]

    print("\n⚖️ Refine Action ################################################################")

    if show_prompt:
        print("\t*******Refining prompt********")
        for chunk in prompt:
            print(chunk['content'])

    new_act = open_ai_chat(prompt=prompt,
                           model="gpt-4-turbo",
                           temperature=0.1,
                           api_key=os.environ["OPENAI_API_KEY"],
                           max_tokens=4096,
                           printing=True, stream=True)

    action_refined = Action()
    action_refined.name = new_act
    action_refined.code = action.code
    action_refined.status = "semi-fixed"

    return action_refined


def check_if_action_achieved(thread_instance: ThreadBase, action: Action, show_prompt: bool = False) -> None:

    """
    check the action and write corresponding code
    """

    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content": f"""
        You are an AI code assistant agent. 
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
        You have an overall long-term goal: {thread_instance.goal},  and your current action is:
        {thread_instance.action_tracked.name}
        
        The code for historical actionflow shown as code are:
        {thread_instance.actionflow.get_code(history=True)}
        
        The code of action in the future are(But you don't need to do this part now, just for your information)):
        {thread_instance.actionflow.get_code(pending=True, current=True)}


        your formally-defined parameters and their previewing are as follows: 
        {thread_instance.exec_environment.preview()}"""},


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


def achieve_action(thread_instance: ThreadBase, action: Action, show_prompt: bool = False) -> Action:

    """
    write code to achieve the action
    """

    # prompt for actionDo **************************************************************************************
    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content": f"""
        You are an AI code assistant agent. 
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
        {thread_instance.tool_box.usable_tools}
    
        Try to understand the meaning of each function and its parameter, and decide the best function and use the function for this step to accomplish the action. 
        """},

        # 3. provide the goal, current action, code history, code future, environment, knowledge
        {"role": "system",
        "content": f"""
        You have an overall long-term goal: {thread_instance.goal},  and your current action is:
        {thread_instance.action_tracked.name}
    
        The code for historical actionflow shown as code are:
        {thread_instance.actionflow.get_code(history=True)}
    
        The code of action in the future are(But you don't need to do this part now, just for your information)):
        {thread_instance.actionflow.get_code(pending=True, current=True)}

        The code you generate will be run, and your formally-defined parameters and their previewing are as follows: 
        {thread_instance.exec_environment.preview()}
        """},


        # 4. provide the code of the action
        {"role": "user",
        "content": f"""
        user have already write some code for this action, but it's not finished. You should replace the XXX.do() part. Don't keep the .do() function after your response. The XXX is your name, and the .do() is an instruction of 'you must write code and put it here'.:
        {action.code}
        Now you write code to achieve your action: {action.name}
        DON'T ASSUME you know the knowledge that you don't know. DON'T ASSUME that you have non-existent functions or hypothetical function, and you can show your thinking and reason in the comment. But don't write any code calling undefined functions in this case.
        make sure that the parameter in your respond code follow the type of the parameter in the function instruction.
        You are NOT allowed to write XXX.do() in your final response as code. When the XXX.do() appears, you HAVE TO change it to other code.
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

    action_plan = Action()
    action_plan.name = action.name
    action_plan.code = new_code
    action_plan.status = "fixed"

    return action_plan
