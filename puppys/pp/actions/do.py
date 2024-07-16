from loguru import logger
from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.pp.actions.explore import explore


def do(
    puppy_instance, 
    action_name: str, 
    model: str = "gpt-4-turbo", 
    show_prompt: bool = False, 
    show_response: bool = False, 
    retries: int = 3
    ) -> str:
    """
    write code to achieve the action
    retry when error occurs, defaulted to 2 times
    """
    history_codes = "\n".join(puppy_instance.actionflow.history_codes)
    future_codes = "\n".join(puppy_instance.actionflow.future_codes)

    prompt = [
        # 1. define your agent type and name
        {"role": "system",
         "content":
             f"""You are an AI code assistant agent. 

1. You always write Python code! You are really good at it. Your natural language output should be written as comment in python code.
you can show your thinking and reason in the comment.
 for example: # Hello, I am an assistant. 

2. DON'T ASSUME you know any unclear knowledge or information that you don't know. DON'T 
 ASSUME that you have non-existent functions or hypothetical function. DON'T ASSUME you know the knowledge that you don't know. 
 Your code will be run immediately after you write it. If you assume any hypothetical function, the the system will crash. 

3. If you cannot do the action, you are allowed to talk to human for help.

4. Your response cannot only be comment. You HAVE to write codes

5. make sure that the parameter in your respond code follow the type of the parameter in the function instruction. You are NOT allowed to write self.do(XXX) 
in your final response as code. When the do(XXX) appears, you HAVE TO change it to other code. your response should be similar with the following example(ONLY CODE) and NOTHING ELSE.
"""},

        # 2. provide the current var and usable tools
        {"role": "user",
         "content":
             f"""Your formally-defined parameters and their previewing are as follows: 
{puppy_instance.puppy_vars.preview()}

You default function is writing python code, it's good at any task that python packages can achieve. But make sure that you write code to import the given package.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them. You are not allowed to call functions that out of the given range and python popular package:
{explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])}

The code for [historical actionflow] are: {history_codes}
The code for [current actionflow]: {puppy_instance.actionflow.current_code}
The code for [future actionflow] are: {future_codes}
Note: The [future actionflow] is for referencing the next steps, you DO NOT need to write code and replace them!
Now you write code to achieve your action(Note that the tools after@ is recommended tools, if it exists): {action_name}

For this action, you have already tried following code, but not finish yet. Think about it, You need to keep writing it.
maybe you should use a different function or try a new way to achieve the action, don't repeat the same code:
{puppy_instance.actionflow.current_action_code}

Try to understand the meaning of each function and its parameter, and decide the best function and use the function 
for this step to accomplish the action. You are only allowed to generate code that replace self.do(\"{action_name}\") and self.do_check(\"{action_name}\") part.
note that before this action is historical code, and it has been ran. You don't need to write historical code again here.

For example: (current action: search the location of the NBA in 2019@ google search @zhihu search)
response:
# To answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
location=google_search("Where is the NBA in 2019")
location= zhihu_search("Where is the NBA in 2019")

Now, there is one more important thing, if there is an error: {puppy_instance.actionflow.errors} (this part might be blank), you
will need to analyse it and try to solve it. When generating the code, you need to try to resolve this.

Now generate your answer as code: 
"""}]

    # prompt finished *****************************************************************************************

    action = Action(puppy_instance, action_name, model, show_prompt, show_response, retries)

    action.highlighting(action_type = "doing_action", prompt = prompt, prompt_action="doing")

    new_code = action.llm_api_call(prompt)

    new_code = action.clean_llm_code(new_code, add_code = True)

    action.replace_action_code(new_code)

    puppy_instance = action.get_puppy_instance()

    # run the code
    try:
        return action.run_without_errors(new_code)

    # if there is an error, try to fix it
    except Exception as e:
        error_details = action.run_with_errors(e)
        if retries <= 0:
            logger.error(f"Puppy is not able to resolve the error: {error_details}")
            return
        else:
            do(puppy_instance, action_name, model, show_prompt, show_response, retries - 1)
    
