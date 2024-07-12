import os
from puppys.env.func_env import FuncEnv
from puppys.llm.open_ai import open_ai_chat
from puppys.pp.actions.explore import explore


def rewrite(puppy_instance, user_prompt: str, show_prompt: bool = False, show_response: bool = False, model: str = "gpt-4o", temperature: float = 0.7, max_tokens: int = 2048) -> str:
    """
    Rewrite user instructions to be more specific and aligned with available tools.
    """
    
    descriptions = explore(environment=puppy_instance.env_node, target=FuncEnv, output_content_mode="attribute", attributes=["name", "description"])
    descriptions_str = "\n".join([f"{tool_name}: {details['description']}" for tool_name, details in descriptions.items()])
    sys_prompt = f"""
    Your job is to rewrite user instructions to be more specific and aligned with available tools. Each user instruction should be transformed into one or more tool actions.

    Here are the available tools:
    {descriptions_str}

    When rewriting the user instructions, ensure each action is clear and corresponds to one of the tools provided. Separate each tool action into its own line.

    Note: You only need to rewrite the instruction as sentences, DO NOT write any code or output any other contents!
    
    Examples:
    User instruction: "Search for the latest news about AI."
    Rewritten instructions:
    1. Use the `news_search` tool to find the latest news about AI.

    User instruction: "Get the weather forecast for tomorrow in San Francisco."
    Rewritten instructions:
    1. Use the `weather_forecast` tool to get the weather forecast, the time is tomorrow and the location is San Francisco.

    Now, rewrite the following user instruction:
    """
    
    prompt_messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    GREEN= "\033[32m"
    RED = "\033[31m"
    GREY = "\033[90m"
    RESET = "\033[0m"

    print(GREEN+"[rewriting_prompt]" + user_prompt + RESET)

    if show_prompt is True:
        print(GREY+"\t*******doing prompt********"+RESET)
        for chunk in prompt_messages:
            print(GREY+chunk['content']+RESET)

    result = open_ai_chat(prompt = prompt_messages,
                          model = model,
                          temperature = temperature,
                          api_key = os.environ["OPENAI_API_KEY"],
                          max_tokens = max_tokens,
                          printing = show_response, 
                          stream = True)

    return result
