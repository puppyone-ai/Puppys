import os
from litellm import completion
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union


@dataclass
class ChatConfig:
    """
    Configuration for the chat service using the litellm interface.
    """

    model: str = 'gpt-4-turbo'
    messages: List[Dict[str, Any]] = field(default_factory=list)
    temperature: float = 0.1
    top_p: Optional[float] = None
    max_tokens: int = 4096
    n: int = 1
    stream: bool = True
    stop: Optional[str] = None
    presence_penalty: Optional[float] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[Dict[int, float]] = None
    seed: Optional[int] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    deployment_id: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    api_version: Optional[str] = None
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[str] = None
    timeout: Optional[Union[float, int]] = None
    user: Optional[str] = None
    response_format: Optional[Dict[str, Any]] = None
    tools: Optional[List[str]] = None
    tool_choice: Optional[str] = None
    parallel_tool_calls: Optional[bool] = None


class ChatService:
    def __init__(
        self, 
        config: ChatConfig
    ):
        self.config = config
        api_key = self.config.api_key
        self.config.api_key = api_key if api_key else os.environ.get("OPENAI_API_KEY", api_key)

    def chat(
        self, 
        printing: bool = False
    ) -> Any:
        """
        Sending prompts to the specified model and returning the response based on the configuration.

        Args:
            printing (bool): Whether to print the response. The default is False.

        Returns:
            Any: The response from the model.
        """

        data = {k: v for k, v in self.config.__dict__.items() if v is not None}
        response = completion(**data)
        return self._handle_response(response, printing)

    def _handle_response(
        self, 
        response: any, 
        printing: bool
    ) -> str:
        """
        Handle the response from the model based on the configuration.

        Args:
            response (any): The response from the model.
            printing (bool): Whether to print the response.

        Returns:
            str: The response content.
        """

        if self.config.stream:
            return self._handle_stream_response(response, printing)
        else:
            return self._handle_non_stream_response(response, printing)

    def _handle_non_stream_response(
        self, 
        response: Any, 
        printing: bool
    ) -> str:
        """
        Handle the non-stream response from the model.

        Args:
            response (Any): The response from the model.
            printing (bool): Whether to print the response.

        Returns:
            str: The response content.
        """

        response_content = response.choices[0].message.content
        if printing:
            print(response_content + "\n")
        return response_content

    def _handle_stream_response(
        self, 
        response: Any, 
        printing: bool
    ) -> str:
        """
        Handle the stream response from the model.

        Args:
            response (Any): The response from the model.
            printing (bool): Whether to print the response.

        Returns:
            str: The response content.
        """

        final_response = ""
        for chunk in response:
            chunk_content = chunk.choices[0].delta.content
            if chunk_content:
                if printing:
                    print(chunk_content, end="")
                final_response += chunk_content
        if printing:
            print("\n")
        return final_response
            

if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    load_dotenv()

    config = ChatConfig(
        messages=[{"role": "user", "content": "Hello, world!"}],
        stream=True,
        temperature=0.7,
    )
    chat_service = ChatService(config)
    result = chat_service.chat(printing=True)
