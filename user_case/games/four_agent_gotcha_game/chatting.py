from __future__ import annotations
from puppys.env.env import Env


class ChattingHistory(Env):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = []

    # Add the chatting content to chat_history
    def add(self, words: str, role: str):
        chatting = {
            "role": role,
            "content": words
        }
        self.value.append(chatting)

    def pop(self, num: int = 0):
        return self.value.pop(num)
