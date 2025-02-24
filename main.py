import websockets
import json
import asyncio
import random
from collections import deque

MAX_MESSAGE_PER_SECOND = 5
MAX_STREAM_PER_CONNECTION = 1024
MAX_CONNECTION_PER_5_MINUTES = 300

class BinanceWebSocket:
    def __init__(self, uri):
        self.uri = uri
        self.send_queue = asyncio.Queue()
        self.current_subscriptions = set()
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.uri, ping_interval=20, ping_timeout=60)
        asyncio.create_task(self.message_sender())
        asyncio.create_task(self.receive_messages())

    async def message_sender(self):
        pass

    async def receive_messages(self):
        pass

    async def subscribe(self):
        pass

    async def unsubscriber(self):
        pass


async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())


#async def binance_connector():
#    uri = "wss://stream.binance.com:9443/ws/btcusdt@trade"
#    async with websockets.connect(uri, ping_interval=20, ping_timeout=60) as websocket:
#        while True:
#            try:
#                msg = await websocket.recv()
#                msg_data = json.loads(msg)
#                print(msg_data)
#            except websockets.exceptions.ConnectionClosed as e:
#                print(e)
#                await asyncio.sleep(5)
#            except Exception as e:
#                print(e)
#                break
#if __name__ == "__main__":
#    asyncio.run(binance_connector())
