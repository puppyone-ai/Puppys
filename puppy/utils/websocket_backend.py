import websockets
import asyncio


# async def send_message_to_frontend(message: str) -> None:
#     async with websockets.connect('ws://localhost/notify') as websocket:
#         await websocket.send(message)


async def request_feedback_from_frontend(message: str) -> str:

    async with websockets.connect('ws://localhost:9001/notify') as websocket:
        await websocket.send(message)

    async with websockets.connect('ws://localhost:9001/feedback') as websocket:
        try:
            async for response in websocket:
                return response
        except websockets.ConnectionClosed:
            # 如果连接关闭，重新连接
            print('Server connection closed')

        except Exception as e:
            # 处理其他可能的异常
            print(f"An error occurred: {e}")
            await asyncio.sleep(1)  # 等待一段时间后重试
    