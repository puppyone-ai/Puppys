import os
from typing import Any
from litellm import completion


class ChatService:
    """
    Chat configurations to interact with LiteLLM's completion API with optional parameters.

    Init Args:
        api_key (str): The API key to use for the OpenAI API. Use the environment variable OPENAI_API_KEY if not provided.
        model (str): The model to use for the LLM. Use the environment variable OPENAI_MODEL if not provided.
        messages (list): List of messages comprising the conversation so far.
        temperature (float, optional): The temperature of the LLM. The higher the temperature, the more random the output. The default is 0.1 for stable responses.
        max_tokens (int, optional): The maximum number of tokens to generate. The default is 4096.
        printing (bool, optional): Whether to print the response. The default is False.
        stream (bool, optional): Whether to stream the response. The default is True.
        top_p (float, optional): Nucleus sampling probability.
        n (int, optional: Number of chat completion choices to generate. The default is 1.
        stop (str or list, optional): Sequences where the API will stop generating further tokens.
        presence_penalty (float, optional): Penalty for new tokens based on their presence.
        frequency_penalty (float, optional): Penalty for new tokens based on their frequency.
        kwargs (dict, optional): Additional parameters for any LLMs API require.

    Returns:
        str: The response from the LiteLLM API.
    """

    def __init__(
        self,
        api_key: str = None,
        model: str = "gpt-4-turbo",
        messages: list = None,
        temperature: float = 0.1, 
        max_tokens: int = 4096,
        printing: bool = False, 
        stream: bool = True,
        top_p: float = None,
        n: int = 1,
        stop: str = None,
        presence_penalty: float = None,
        frequency_penalty: float = None,
        **kwargs
    ):  
        self.api_key = api_key if api_key else os.environ.get("OPENAI_API_KEY", api_key)
        self.model = model if model else os.environ.get("OPENAI_MODEL", model)

        if not messages:
            raise ValueError("The messages field is required for the chat completion tasks with the specific LLM.")

        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.printing = printing
        self.stream = stream
        self.top_p = top_p
        self.n = n
        self.stop = stop
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty

        # Set any additional attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def chat_completion(
        self, 
    ) -> Any:
        """
        Sending prompts to the specified model and returning the response based on the configuration.

        Args:
            printing (bool): Whether to print the response. The default is False.

        Returns:
            Any: The response from the model.
        """

        data = {k: v for k, v in self.__dict__.items() if v is not None and k != "printing"}
        response = completion(**data)
        if self.stream:
            return self._handle_stream_response(response)
        else:
            return self._handle_non_stream_response(response)

    def _handle_non_stream_response(
        self, 
        response: Any, 
    ) -> str:
        """
        Handle the non-stream response from the model.

        Args:
            response (Any): The response from the model.

        Returns:
            str: The response content.
        """

        response_content = response.choices[0].message.content
        if self.printing:
            print(response_content + "\n")
        return response_content

    def _handle_stream_response(
        self, 
        response: Any
    ) -> str:
        """
        Handle the stream response from the model.

        Args:
            response (Any): The response from the model.

        Returns:
            str: The response content.
        """

        final_response = ""
        for chunk in response:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content:
                if self.printing:
                    print(chunk_content, end="")
                final_response += chunk_content
        if self.printing:
            print("\n")
        return final_response


def lite_llm_chat(
    **kwargs
) -> str:
    """
    The main function to interact with the litellm interface and generate responses based on the configuration.

    Args:
        **kwargs: The keyword arguments for the chat configurations, including:
        - api_key
        - model
        - messages
        - temperature
        - max_tokens
        - printing
        - stream
        - top_p
        - n
        - stop
        - presence_penalty
        - frequency_penalty
        - kwargs

    Returns:
        str: The response content.
    """

    # Initialize the ChatService with the configured settings
    chat_service = ChatService(**kwargs)

    try:
        # Call the chat method and print the results if printing is set to True
        result = chat_service.chat_completion()
    except Exception as e:
        raise ValueError(f"Error in Lite LLM chat completion: {e}")

    # Return the result from the chat service
    return result
            

if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    load_dotenv()
    result = lite_llm_chat(
        messages=[{"role": "user", "content": "Hello, world!"}],
        stream=True,
        temperature=0.7,
        printing=True
    )
    print(result)
