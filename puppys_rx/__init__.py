import asyncio
import websockets


notify_message_queue = asyncio.Queue()
feedback_message_queue = asyncio.Queue()


async def websocket_recv_handler(websocket, path):
    while True:
        message = await websocket.recv()
        print(f'Received message: {message}')
        await notify_message_queue.put(message)
        await asyncio.sleep(1)


async def websocket_send_handler(websocket, path):
    while True:
        message = await feedback_message_queue.get()
        await websocket.send(message)
        # await websocket.send("hello")
        print(f'Sent message: hello')
        await asyncio.sleep(1)


async def handle_websocket(websocket, path):
    if path == "/notify":
        await websocket_recv_handler(websocket, path)
    elif path == "/feedback":
        await websocket_send_handler(websocket, path)


# if __name__ == "__main__":
#     asyncio.gather(start_websocket_server())
#     asyncio.run(start_websocket_server())
