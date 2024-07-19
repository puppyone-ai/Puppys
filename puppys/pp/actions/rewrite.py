from puppys.env.func_env import FuncEnv
from puppys.pp.actions.action import Action
from puppys.pp.actions.explore import explore


def rewrite(
    puppy_instance: any, 
    user_prompt: str, 
    show_prompt: bool = False, 
    show_response: bool = False, 
    model: str = "gpt-4o", 
    temperature: float = 0.7, 
    max_tokens: int = 512
) -> str:
    """
    Rewrite user instructions to be more specific and aligned with available tools.

    Args:
        puppy_instance (any): The puppy instance.
        user_prompt (str): The user prompt to rewrite.
        show_prompt (bool): Whether to show the prompt. The default is False.
        show_response (bool): Whether to show the response. The default is False.
        model (str): The model to use for the Large Language Model. The default is "gpt-4o".
        temperature (float): The temperature of the Large Language Model. The default is 0.7.
        max_tokens (int): The maximum number of tokens to generate. The default is 512.

    Returns:
        str: The rewritten user instructions.
    """
    
    descriptions = explore(
        environment=puppy_instance.env_node, 
        target=FuncEnv, 
        output_content_mode="attribute", 
        attributes=["name", "description"]
    )
    descriptions_str = "\n".join(
        [f"{tool_name}: {details['description']}" for tool_name, details in descriptions.items()]
    )
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
    
    action = Action(
        puppy_instance, 
        user_prompt, 
        model, 
        show_prompt, 
        show_response, 
        retries=0
    )

    action.highlighting("rewriting_prompt", prompt_messages)

    result = action.llm_api_call(prompt_messages, temperature, max_tokens)

    rewrite_replace = "rewrote_action = \"" + result.replace("\n", "\\n") + "\""
    action.replace_action_code(rewrite_replace)

    return result
