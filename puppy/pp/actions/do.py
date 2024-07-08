from puppy.llm.open_ai import open_ai_chat
from puppy.env.func_env import FuncEnv
from puppy.pp.actions.explore import explore
import os
import re


def write_to_py_file(code: str):
    """
    Write the code to a python file
    """
    root_path = "TempActionCode"
    file_name = "temp_decision_tree_code.py"

    if not os.path.exists(root_path):
        os.makedirs(root_path)

    file_path = os.path.join(root_path, file_name)

    # write the code inside a function
    code_with_indentation = "\n".join(["    " + line for line in code.split("\n")])
    code = f"def decisiontree(self):\n" + code_with_indentation

    with open(file_path, "w") as f:
        f.write(code + '\n')


def do(puppy_instance, action_name: str, model="gpt-4-turbo", show_prompt=False, show_response=False):
    """
    write code to achieve the action
    """

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

The code for historical, current, and future actionflow shown as code are:{puppy_instance.actionflow.all_code}
Now you write code to achieve your action(Note that the tools after@ is recommended tools, if it exists): {action_name}

For this action, you have already tried following code, but not finish yet. Think about it, You need to keep writing it.
maybe you should use a different function or try a new way to achieve the action, don't repeat the same code:
{puppy_instance.actionflow.current_action_code}

Try to understand the meaning of each function and its parameter, and decide the best function and use the function 
for this step to accomplish the action. You are only allowed to generate code that replace self.do({action_name}) part.
note that before this action is historical code, and it has been ran. You don't need to write historical code again here.

For example: (current action: search the location of the NBA in 2019@ google search @zhihu search)
response:
# To answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
location=google_search("Where is the NBA in 2019")
location= zhihu_search("Where is the NBA in 2019")

Now generate your answer as code: 
"""}]

    # prompt finished *****************************************************************************************

    print("[doing_action]" + action_name)

    if show_prompt is True:
        print("\t*******planning prompt********")
        for chunk in prompt:
            print(chunk['content'])

    new_code = open_ai_chat(prompt=prompt,
                            model=model,
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=show_response, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    # add the ran code into the current code until the checking result is true
    puppy_instance.actionflow.current_action_code += new_code
    puppy_instance.actionflow.current_action_code += "\n"

    # replace the action code in the all code
    all_code = puppy_instance.actionflow.all_code
    for action in all_code.split("\n"):
        leading_whitespaces = re.match(r"\s*", action).group()
        if action_name in action:
            new_code_to_add = "\n".join([leading_whitespaces + line for line in new_code.split("\n")]) + "\n"
            puppy_instance.actionflow.all_code = all_code.replace(action, new_code_to_add)
            break

    # write new code to a temp python file
    write_to_py_file(puppy_instance.actionflow.all_code)

    # run the code
    puppy_instance.actionflow.puppy_exec(new_code)

    return new_code
