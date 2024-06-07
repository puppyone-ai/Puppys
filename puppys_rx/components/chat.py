import reflex as rx

from puppys_rx.components import loading_icon
from puppys_rx.state import Q, A, State
from typing import Union


message_style = dict(
    display="inline-block",
    padding="1em",
    border_radius="8px",
    max_width=["30em", "30em", "50em", "50em", "50em", "50em"],
    margin_y="0.5em",
    box_shadow="rgba(0, 0, 0, 0.15) 0px 2px 8px",
)


# def message_q(q: Q) -> rx.Component:
#     """
#     A single question message.
#
#     Args:
#         q: The question.
#
#     Returns:
#         A component displaying the question.
#     """
#     return rx.box(
#             rx.markdown(
#                 q.question,
#                 background_color=rx.color("mauve", 4),
#                 color=rx.color("mauve", 12),
#                 **message_style,
#             ),
#             text_align="right",
#             margin_top="1em",
#         )


def message(qa: Union[Q, A]) -> rx.Component:
    """A single answer message.

    Args:
        qa: The answer or question.

    Returns:
        A component displaying the answer.
    """

    text_box = None

    if isinstance(qa, Q):
        text_box = rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("mauve", 4),
                color=rx.color("mauve", 12),
                **message_style,
            ),
            text_align="right",
            margin_top="1em",
            width="100%",
        )

    if isinstance(qa, A):
        text_box = rx.box(
            rx.markdown(
                qa.question,
                background_color=rx.color("accent", 4),
                color=rx.color("accent", 12),
                **message_style,
            ),
            text_align="left",
            padding_top="1em",
            width="100%",
        )

    return rx.box(text_box) if text_box else rx.box()


def chat() -> rx.Component:
    """List all the messages in a single conversation."""

    return rx.vstack(
        rx.box(
            rx.foreach(
                State.chats[State.current_chat],
                message
            ),
            width="100%"),
        py="8",
        flex="1",
        width="100%",
        max_width="50em",
        padding_x="4px",
        align_self="center",
        overflow="hidden",
        padding_bottom="5em",
    )


def action_bar() -> rx.Component:
    """The action bar to send a new message."""
    return rx.center(
        rx.vstack(
            rx.chakra.form(
                rx.chakra.form_control(
                    rx.hstack(
                        # rx.radix.text_field.root(
                        rx.input(
                            placeholder="Ask puppy...",
                            id="question",
                            width=["10em", "15em", "20em", "30em", "40em", "50em"],
                            height="3em",
                            borderRadius="13px",
                        ),
                            # rx.radix.text_field.slot(
                            #     rx.tooltip(
                            #         rx.icon("info", size=18),
                            #         content="Enter a question to get a response.",
                            #     )
                            # ),
                        # ),
                        rx.button(
                            rx.cond(
                                State.processing,
                                loading_icon(height="1em"),
                                rx.text("Send"),
                            ),
                            type="submit",
                        ),
                        align_items="center",
                    ),
                    is_disabled=State.processing,
                ),
                on_submit=State.send_human_feedback_by_websocket,
                reset_on_submit=True,
            ),
            # rx.text(
            #     "ReflexGPT may return factually incorrect or misleading responses. Use discretion.",
            #     text_align="center",
            #     font_size=".75em",
            #     color=rx.color("mauve", 10),
            # ),
            # rx.logo(margin_top="-1em", margin_bottom="-1em"),
            # align_items="center",
        ),
        position="sticky",
        bottom="0",
        left="0",
        padding_y="16px",
        backdrop_filter="auto",
        backdrop_blur="lg",
        border_top=f"1px solid {rx.color('gray', 3)}",
        background_color=rx.color("gray", 2),
        align_items="stretch",
        width="100%",
    )
