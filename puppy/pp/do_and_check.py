from puppy.pp.base import   PuppyBase
from puppy.llm.openAI import open_ai_chat
import os

def do(puppy_instance:PuppyBase, action_name: str = "", tool_list: list = [], show_prompt=False, show_response=False):
    """
    write code to achieve the action
    """
    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content":
             f"""You are an AI code assistant agent. 

1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
 for example: # Hello, I am an assistant. 

2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T 
 ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately 
 after you write it. If you assume any hypothetical function, the the system will crash. 

3. If you cannot do the action, you are allowed to send message to user for help.

4. Your response cannot only be comment. You HAVE to write codes
"""},

        # 2. provide the current var and usable tools
        {"role": "system",
         "content":
             f"""The code you generate will be run, and your formally-defined parameters and their previewing are as follows: 
{puppy_instance.vars_preview}

You default function is writing python code, it's good at any task that python packages can achieve. But make sure that you write code to import the given package.
You are also allowed to use the customized functions below:
{puppy_instance.tool_box.detail}
 """},

        # 2. provide the goal, current action, code history, code future, environment, knowledge
        {"role": "system",
         "content":
             f"""and your current action is:
{action_name}

The code for historical, current, and future actionflow shown as code are:
{puppy_instance.actionflow.all_code}

Now you write code to achieve your action(Note that the tools after@ is recommended tools, if it exists): 
{action_name}

For this action, you have already tried following code, but not finish yet. Think about it, maybe you should use a different function or
try a new way to achieve the action, don't always repeat the same action:
{puppy_instance.actionflow.current_code}

Try to understand the meaning of each function and its parameter, and decide the best function and use the function 
for this step to accomplish the action. You are only allowed to generate code that replace self.do({action_name}) part.
For example: (current action: search the location of the NBA in 2019@ google search @zhihu search)
response:
# To answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
location=google_search("Where is the NBA in 2019"
location= zhihu_search("Where is the NBA in 2019")"""},

        # 4. provide the code of the action
        {"role": "user",
         "content":
             f"""DON'T ASSUME you know the knowledge that you don't know. 
DON'T ASSUME that you have non-existent functions or hypothetical function, and you can show your thinking and reason 
in the comment. But don't write any code calling undefined functions in this case. make sure that the parameter in 
your respond code follow the type of the parameter in the function instruction. You are NOT allowed to write self.do(XXX) 
in your final response as code. When the do(XXX) appears, you HAVE TO change it to other code. your response should 
be similar with the example(ONLY CODE) and NOTHING ELSE. """}]

    # prompt finished *****************************************************************************************

    print("[doing_action]" + action_name)

    if show_prompt:
        print("\t*******planning prompt********")
        for chunk in prompt:
            print(chunk['content'])

    new_code = open_ai_chat(prompt=prompt,
                            model="gpt-4-turbo",
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=show_response, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    puppy_instance.actionflow.current_code += new_code

    puppy_instance.puppy_exec(new_code)

    return new_code


def check(puppy_instance: PuppyBase, action_name: str = "", tool_list: list = [], show_prompt=False, show_response=False):
    """
    check if it finish or not
    """
    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content":
             f"""You are an AI code assistant agent. 

    1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
     for example: # Hello, I am an assistant. 

    2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T 
     ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately 
     after you write it. If you assume any hypothetical function, the the system will crash. 

    3. Your response cannot only be comment. You HAVE to write codes
    """},

        # 2. set the standard of if the action is done or not
        {"role": "system",
         "content": f""" You justify if your current action is done or not, you have two choices: 1. Done: That means 
    you don't need to write code to achieve it again. The action history shows that you have already know what 
    you want to know or have already achieve the action. In this case, you should write Python code to return 
    Ture, and your generated code should be: isFinished=True

    2. Unfinished: That means you need to write code to achieve it again, or there are some unfinished actions that you 
    need to make . In this case, you should write Python code to return False, and the your generated code should be: 
    isFinished=False

    for example:
    1. current action:
    发信息给我妈妈 @ask for help
    current code:
    # Since I don't have any information about the user's mother or the content of the message, I need to ask the user for help.
    message_content = XiaoMei.askHumanForHelp.run("What message would you like to send to your mom?")
    # the user claimed that the message is "I love you mom"

    your response:
    # the action is not done, because I get what I should send, but I haven't send it yet. Maybe next action is to send it
    isFinished=False

    2. current action:
    get what happened about COVID in the the 2nd Feb 2020 @google search
    current code:
    # I need to search the information about what happened in the the 2nd Feb 2020. The function returns as a string.
    result=google_search("What happened in the the 2nd Feb 2020")
    # the result is "First death resulting from Coronavirus outside China reported."

    your response:
    # I get what I should get, and I don't need to do anything else if there is no other action provide by human.
    isFinished=True"""},

        # 2. provide the current var and usable tools
        {"role": "system",
         "content":
             f"""Your formally-defined parameters and their previewing are as follows: 
    {puppy_instance.vars_preview}

    The code for historical, current, and future actionflow shown as code are:
    {puppy_instance.actionflow.all_code}

    Now you are at this action: 
    {action_name}

    For this action, you have already tried:
    {puppy_instance.actionflow.current_code}

    Try to understand the meaning of each function and its parameter, before you are sure that one action has been finished, 
    think about if you can find the corresponding defined parameters and its reasonable value that in this environment.
    and Now you need to write code to justify if the action of {action_name} is done or not:
    Your response should be similar to the response example(ONLY CODE, and COMMENT) and NOTHING ELSE."""}]

    print("[checking_action]" + action_name)

    if show_prompt:
        print("\t*******planning prompt********")
        for chunk in prompt:
            print(chunk['content'])

    new_code = open_ai_chat(prompt=prompt,
                            model="gpt-4-turbo",
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=show_response, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    puppy_instance.puppy_exec(new_code)

    if puppy_instance.runtime_vars_dict["isFinished"] == True:
        puppy_instance.actionflow.current_code = ""

    return puppy_instance.runtime_vars_dict["isFinished"]


def do_check(puppy_instance: PuppyBase, action_name: str = "", tool_list: list = [], show_prompt=False, show_response=False):
    puppy_instance.runtime_vars_dict["isFinished"] = False

    while puppy_instance.runtime_vars_dict["isFinished"] == False:
        puppy_instance.do(action_name, tool_list, show_prompt, show_response)
        puppy_instance.check(action_name, tool_list, show_prompt, show_response)

    puppy_instance.actionflow.current_code = ""