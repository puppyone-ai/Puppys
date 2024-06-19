from puppy.llm.openAI import open_ai_chat
from puppy.env.func_env import FuncEnv
import os


def do(puppy_instance, action_name: str, tool_list: list, show_prompt=False, show_response=False):

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
{puppy_instance.vars_preview}

You default function is writing python code, it's good at any task that python packages can achieve. But make sure that you write code to import the given package.
You are also allowed to use the customized functions below, use them by just writing code as the example. the description shows how to use them.
{puppy_instance.explore(puppy_instance, target=FuncEnv, sub_only=True)}

The code for historical, current, and future actionflow shown as code are:{puppy_instance.all_code}.
Now you write code to achieve your action(Note that the tools after@ is recommended tools, if it exists): {action_name}

For this action, you have already tried following code, but not finish yet. Think about it, maybe you should use a different function or
try a new way to achieve the action, don't always repeat the same action:
{puppy_instance.current_code}

Try to understand the meaning of each function and its parameter, and decide the best function and use the function 
for this step to accomplish the action. You are only allowed to generate code that replace self.do({action_name}) part.
note that before this action is historical code, and it has been ran. You don't need to write historical code again here.

For example: (current action: search the location of the NBA in 2019@ google search @zhihu search)
response:
# To answer where is the NBA in 2019, I need to search the information about NBA in 2019. The function returns as a string.
location=google_search("Where is the NBA in 2019"
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
                            model="gpt-4-turbo",
                            temperature=0.1,
                            api_key=os.environ["OPENAI_API_KEY"],
                            max_tokens=4096,
                            printing=show_response, stream=True)

    new_code = new_code.replace("```python\n", "").replace("\n```", "")

    puppy_instance.current_code += new_code
    puppy_instance.puppy_exec(new_code)

    return new_code
