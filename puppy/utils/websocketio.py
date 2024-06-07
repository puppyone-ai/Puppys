import asyncio
import websockets
import threading


notify_message_queue = asyncio.Queue()
feedback_message_queue = asyncio.Queue()

frontend_clients = set()
puppys_clients = set()


async def websocket_recv_handler(websocket, path):
    frontend_clients.add(websocket)

    try:
        async for message in websocket:
            print(f'Received message from backend: {message}')
            await notify_message_queue.put(message)
            print(f'Put the message into queue yet.')
            await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed normally.")
        await asyncio.sleep(5)

    finally:
        frontend_clients.remove(websocket)


async def websocket_send_handler(websocket, path):
    frontend_clients.add(websocket)
    try:
        while True:
            message = notify_message_queue.get()
            for client in frontend_clients:
                await client.send(message)
            # await websocket.send("hello")
            print(f'Broadcast message to frontend pages: {message}')
            notify_message_queue.task_done()
            await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        frontend_clients.remove(websocket)


async def handle_websocket(websocket, path):
    if path == "/notify":
        await websocket_recv_handler(websocket, path)
    elif path == "/feedback":
        await websocket_send_handler(websocket, path)
    elif path ==


async def start_websocket_server():
    try:
        server = await websockets.serve(handle_websocket, 'localhost', 9001)
        print("WebSocket server started on ws://localhost:9001")
        await server.wait_closed()
    except OSError as e:
        print(f"Failed to start WebSocket server: {e}")


def start_sever():
    loop = asyncio.new_event_loop()

    def start_websocket():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_websocket_server())

    server_thread = threading.Thread(target=start_websocket, daemon=True)
    server_thread.start()


# if __name__ == "__main__":
#     asyncio.gather(start_websocket_server())
#     asyncio.run(start_websocket_server())
