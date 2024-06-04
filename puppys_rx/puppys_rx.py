"""The main Chat app."""
import asyncio

import reflex as rx
from puppys_rx.components import chat, navbar
# from puppys_rx import start_websocket_server
from puppys_rx.state import State


# @rx.page(on_load=State.start_websocket_server)
def index() -> rx.Component:
    """The main app."""
    return rx.chakra.vstack(
        # navbar(),
        chat.chat(),
        chat.action_bar(),
        background_color=rx.color("gray", 1),
        color=rx.color("gray", 12),
        min_height="100vh",
        align_items="stretch",
        spacing="0",
    )


# Add state and page to the app.
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="violet",
    ),
)
app.add_page(index)

# import asyncio
# #
# loop = asyncio.get_event_loop()
# task = asyncio.run_coroutine_threadsafe(start_websocket_server(), loop)
