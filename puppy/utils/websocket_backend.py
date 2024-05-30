import websockets


async def send_message_to_frontend(message: str) -> None:
    async with websockets.connect('ws://localhost:9000/notify') as websocket:
        await websocket.send(message)


async def recv_message_from_frontend(message: str) -> str:
    await send_message_to_frontend(message)
    async with websockets.connect('ws://localhost:9000/feedback') as websocket:
        response = await websocket.recv()
        return response
    