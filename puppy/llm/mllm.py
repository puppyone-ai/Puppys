from mllm import Chat
from halo import Halo
import os


def mllm_chat(prompt,
              model="",
              emoji=False, emoji_text="generating", spinner="moon",
              printing=False):

    client = Chat()

    client += prompt

    if emoji:
        spinner = Halo(text=emoji_text, spinner=spinner)
        spinner.start()

    # Spinning until the message I/O

    res = client.complete(model=model)

    # message I/O done

    if emoji:
        spinner.stop()

    if printing:
        print(res)
        print("\n")

    return res


if __name__ == "__main__":
    response = mllm_chat(prompt="Introduce yourself, with 20 words",
                         printing=True, emoji=True)
