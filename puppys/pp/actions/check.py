from puppys.pp.actions.action import Action
from puppys.llm.models import lite_llm_chat


def check(
    puppy_instance: any,
    action_name: str = "",
    model: str = "gpt-4-turbo",
    show_prompt: bool = False,
    show_response: bool = False
) -> bool:
    """
    Check if the current action has finished by comparing the action prompt and action code.

    Args:
        puppy_instance (any): The puppy instance.
        action_name (str): The name of the action. The default is an empty string.
        model (str): The model to use for the Large Language Model. The default is "gpt-4-turbo".
        show_prompt (bool): Whether to show the prompt. The default is False.
        show_response (bool): Whether to show the response. The default is False.

    Returns:
        bool: The response from the Large Language Model. Expected to be `True` or `False`.
    """

    history_codes = "\n".join(puppy_instance.actionflow.history_codes)
    future_codes = "\n".join(puppy_instance.actionflow.future_codes)

    prompt = [
        # 1. Define your agent type and name
        {"role": "system",
         "content": """
You are an AI code assistant agent. 

1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
    For example: # Hello, I am an assistant. 

2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T 
    ASSUME that you have non-existent functions or hypothetical function. Your code will be run immediately 
    after you write it. If you assume any hypothetical function, then the system will crash. 

3. Your response cannot only be comment. You HAVE to write codes!

    You justify if your current action is done or not, you have two choices: 
    a. Done: That means you don't need to write code to achieve it again. The action history shows that you have already know what 
you want to know or have already achieve the action. In this case, you should write Python code to return 
Ture, and your generated code should be: isFinished = True 
    b. Unfinished: That means you need to write code to achieve it again, or there are some unfinished actions that you 
need to make. In this case, you should write Python code to return False, and the your generated code should be: 

isFinished = False

4. You can only write code that contain True or False. You CANNOT write code that contains or import other values or other code.

For example:
1. Current action:
发信息给我妈妈 @ask for help
Current code:
# Since I don't have any information about the user's mother or the content of the message, I need to ask the user for help.
message_content = XiaoMei.askHumanForHelp.run("What message would you like to send to your mom?")
# The user claimed that the message is "I love you mom"

Your response:
# The action is not done, because I get what I should send, but I haven't send it yet. Maybe next action is to send it
isFinished = False 

2. Current action:
Get what happened about COVID in the the 2nd Feb 2020 @google search
Current code:
# I need to search the information about what happened in the the 2nd Feb 2020. The function returns as a string.
result = google_search("What happened in the the 2nd Feb 2020")
# The result is "First death resulting from Coronavirus outside China reported."

Your response:
# I get what I should get, and I don't need to do anything else if there is no other action provide by human.
isFinished = True
"""},
        # 2. Provide the current var and usable tools
        {"role": "user",
         "content": f"""
Your formally-defined parameters and their previewing are as follows: 
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
Your response should be similar to the response example(ONLY CODE, and COMMENT) and NOTHING ELSE.
"""}]

    action = Action(
        puppy_instance,
        action_name,
        show_prompt,
        show_response,
        retries=0,
        replace_code=False
    )

    action.highlighting(
        action_type="checking_action",
        prompt=prompt,
        prompt_action="checking"
    )

    new_code = lite_llm_chat(
        messages=prompt,
        model=model,
        printing=show_response, 
        stream=True
    )

    new_code = action.clean_llm_code(new_code, add_code=False)

    puppy_instance = action.get_puppy_instance()

    puppy_instance.actionflow.puppy_exec(new_code)

    return puppy_instance.puppy_vars.runtime_dict["isFinished"]
