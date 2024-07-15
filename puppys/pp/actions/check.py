from puppys.llm.open_ai import open_ai_chat
from loguru import logger
import os


def check(puppy_instance, action_name: str = "", model="gpt-4-turbo",show_prompt=False, show_response=False):
    """
    check if it finished or not
    """
    history_codes = "\n".join(puppy_instance.actionflow.history_codes)
    future_codes = "\n".join(puppy_instance.actionflow.future_codes)
    
    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content":
             f"""You are an AI code assistant agent. 

    1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
     for example: # Hello, I am an assistant. 

    2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T 
     ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately 
     after you write it. If you assume any hypothetical function, then the system will crash. 

    3. Your response cannot only be comment. You HAVE to write codes

     You justify if your current action is done or not, you have two choices: 
        a. Done: That means you don't need to write code to achieve it again. The action history shows that you have already know what 
    you want to know or have already achieve the action. In this case, you should write Python code to return 

    Ture, and your generated code should be: isFinished=True 
        b. Unfinished: That means you need to write code to achieve it again, or there are some unfinished actions that you 
    need to make . In this case, you should write Python code to return False, and the your generated code should be: 

    isFinished=False
    
    4. You can only write code that contain True or False. You CANNOT write code that contains or import other values or other code.

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
        {"role": "user",
         "content":
             f"""Your formally-defined parameters and their previewing are as follows: 
    {puppy_instance.puppy_vars.preview()}

    The code for [historical actionflow] are: {history_codes}
    The code for [current actionflow]: {puppy_instance.actionflow.current_code}
    The code for [future actionflow] are: {future_codes}
    Note: The [future actionflow] is for referencing the next steps, you DO NOT need to write code and replace them!

    Now you are at this action: 
    {action_name}

    For this action, you have already tried:
    {puppy_instance.actionflow.current_action_code}

    Try to understand the meaning of each function and its parameter, before you are sure that one action has been finished, 
    think about if you can find the corresponding defined parameters and its reasonable value that in this environment.
    and Now you need to write code to justify if the action of {action_name} is done or not:
    Your response should be similar to the response example(ONLY CODE, and COMMENT) and NOTHING ELSE."""}]

    YELLOW = "\033[33m"
    GREY = "\033[90m"
    RESET = "\033[0m"
    print(YELLOW+"[checking_action]" + action_name + RESET)

    if show_prompt is True:
        # print(f"\t*******planning prompt********")
        print(GREY+f"\t*******checking prompt********"+RESET)
        for chunk in prompt:
            # print(chunk['content'])
            print(GREY+chunk['content']+RESET)

    new_code = open_ai_chat(prompt=prompt,
                            model=model,
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=show_response, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    puppy_instance.actionflow.puppy_exec(new_code)

    return puppy_instance.puppy_vars.runtime_dict["isFinished"]
