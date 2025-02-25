import websockets
import json
import asyncio
import random


MAX_MESSAGE_PER_SECOND = 5
MAX_STREAMS_PER_CONNECTION = 1024
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
        while True:
            messages_sent = 0
            while messages_sent < MAX_MESSAGE_PER_SECOND:
                try:
                    message = self.send_queue.get_nowait()
                    await self.websocket.send(message)
                    print(f"Message: {message}")
                    messages_sent += 1
                except asyncio.QueueEmpty:
                    break
            await asyncio.sleep(1)

    async def receive_messages(self):
        async for message in self.websocket:
            print(f"Message Received {message}")

    async def subscribe(self, stream):

        if len(self.current_subscriptions) >= MAX_STREAMS_PER_CONNECTION:
            print("Limit of Streams")
            return
        if stream in self.current_subscriptions:
            print(f"Already subscribe in: {stream}")
            return

        self.current_subscriptions.add(stream)
        subscribe_message = json.dumps({
            "method": "SUBSCRIBE",
            "params": [stream],
            "id": random.randint(1, 1000000)
        })
        await self.send_queue.put(subscribe_message)
        print(f"Request for subscribe in: {stream} sent")

    async def unsubscriber(self, stream):
        if stream not in self.current_subscriptions:
            print(f"Don't subscribed: {stream}")
            return

        self.current_subscriptions.remove(stream)
        unsubscribe_message = json.dumps({
            "method": "UNSUBSCRIBE",
            "params": [stream],
            "id": random.randint(1, 1000000)
        })
        await self.send_queue.put(unsubscribe_message)
        print(f"Request fom unsubscribe in: {stream} sent")


async def main():
    client = BinanceWebSocket("wss://stream.binance.com:9443/ws")
    await client.connect()
    await client.subscribe("btcusdt@trade")
    await asyncio.sleep(60)  # keeping the connection (60 seconds) to receive messages

if __name__ == "__main__":
    asyncio.run(main())
