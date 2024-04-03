from mllm import Chat
from mllm.provider_switch import set_default_to_anthropic, set_default_to_google, set_default_to_openai


def m_chat(prompt,
           model: str = None, expensive: bool = False,
           printing: bool = False) -> str:

    client = Chat()

    if model:

        match model:
            case "gemini":
                set_default_to_google()
            case "gpt":
                set_default_to_openai()
            case "claude":
                set_default_to_anthropic()

    client += prompt

    res = client.complete(model=model, expensive=expensive)

    # message I/O done

    if printing:
        print(res)
        print("\n")

    return res


if __name__ == "__main__":
    response = m_chat(
        prompt="Introduce yourself, with 20 words",
        printing=True)
