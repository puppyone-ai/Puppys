import os
import queue
import websockets
import asyncio

import reflex as rx
from typing import Union

# # Checking if the API key is set properly
# if not os.getenv("OPENAI_API_KEY"):
#     raise Exception("Please set OPENAI_API_KEY environment variable.")


class Q(rx.Base):
    """A question from human."""

    question: str


class A(rx.Base):
    """An answer from agent."""

    question: str


DEFAULT_CHATS = {
    "Mei": [],
}


class State(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[Union[Q, A]]] = DEFAULT_CHATS

    # The current chat name.
    current_chat: str = "Mei"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = True

    # The name of the new chat.
    new_chat_name: str = ""

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    def load(self):
        async def compose_server():
            async with websockets.serve(self.handler, 'localhost', 9000):
                await asyncio.Future()

        self.message_queue = asyncio.Queue()

        asyncio.create_task(compose_server())

    async def handler(self, websocket, path):
        if path == "/notify":
            await self.recv_massage(websocket)
        elif path == "/feedback":
            await self.send_massage(websocket)

    @rx.background
    async def recv_massage(self, websocket):
        while True:
            message = await websocket.recv()
            self.chats[self.current_chat].append(A(question=message))

    @rx.background
    async def send_massage(self, websocket):
        while True:
            message = await self.message_queue.get()  # 从队列中获取消息
            await websocket.send(message)

    async def send_human_feedback(self, form_data: dict[str, str]):
        """
                Args:
                    form_data: A dict with the current question.
        """

        # Toggle the processing flag.
        self.processing = False
        yield

        # Get the question from the form
        human_feedback = form_data["question"]

        # Check if the question is empty
        if human_feedback == "":
            return

        await self.message_queue.put(human_feedback)
        self.chats[self.current_chat].append(Q(question=human_feedback))

        # Clear the input and start the processing.
        self.processing = True


# message_queue = asyncio.Queue()

#
# async def compose_server():
#     async with websockets.serve(State.handler, 'localhost', 9000):
#         await asyncio.Future()
#
#
# asyncio.run(compose_server())
