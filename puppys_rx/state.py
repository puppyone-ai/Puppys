import asyncio

import reflex as rx
from typing import Union
from puppys_rx import notify_message_queue, feedback_message_queue, handle_websocket

import websockets
# from puppy.tools.defaultTools.send_message_to_human import notify_message_queue, feedback_message_queue


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

    @rx.background
    async def start_websocket_server(self):
        server = await websockets.serve(handle_websocket, 'localhost', 9001)
        print("WebSocket server started on ws://localhost:9001")
        await server.wait_closed()

    @rx.background
    async def recv_message_by_websocket(self):
        while True:
            """Receive a message from the server."""
            if not notify_message_queue.empty():
                message = await notify_message_queue.get()
                print(message)
                async with self:
                    self.chats[self.current_chat].append(A(question=message))
                    self.processing = False
            await asyncio.sleep(3)

    async def send_human_feedback_by_websocket(self, form_data: dict[str, str]):
        """
                Args:
                    form_data: A dict with the current question.
        """

        # Get the question from the form
        human_feedback = form_data["question"]

        # Check if the question is empty
        if human_feedback == "":
            return

        await feedback_message_queue.put(human_feedback)
        self.chats[self.current_chat].append(Q(question=human_feedback))

        # Clear the input and start the processing.
        self.processing = True

    # @rx.background
    # async def recv_message_by_queue(self):
    #     while True:
    #         """Receive a message from the server."""
    #         if not notify_message_queue.empty():
    #             message = await asyncio.to_thread(notify_message_queue.get)
    #             print(message)
    #             async with self:
    #                 self.chats[self.current_chat].append(A(question=message))
    #                 self.processing = False
    #         await asyncio.sleep(3)
    #
    # async def send_human_feedback_by_queue(self, form_data: dict[str, str]):
    #     """
    #             Args:
    #                 form_data: A dict with the current question.
    #     """
    #
    #     # Get the question from the form
    #     human_feedback = form_data["question"]
    #
    #     # Check if the question is empty
    #     if human_feedback == "":
    #         return
    #
    #     # await send_message_queue.put(human_feedback)
    #     await asyncio.to_thread(feedback_message_queue.put, human_feedback)
    #     # await self.send_massage()
    #     self.chats[self.current_chat].append(Q(question=human_feedback))
    #
    #     # Clear the input and start the processing.
    #     self.processing = True
