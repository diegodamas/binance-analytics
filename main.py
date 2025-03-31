import websockets
import json
import asyncio
import random
import signal
from message_connector import send_message


MAX_MESSAGE_PER_SECOND = 5
MAX_STREAMS_PER_CONNECTION = 1024
MAX_CONNECTION_PER_5_MINUTES = 300


class BinanceWebSocket:
    def __init__(self, uri):
        self.uri = uri
        self.send_queue = asyncio.Queue()
        self.current_subscriptions = set()
        self.websocket = None
        self.shutdown_event = asyncio.Event()

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri, ping_interval=20, ping_timeout=60)
            asyncio.create_task(self.message_sender())
            asyncio.create_task(self.receive_messages())
        except Exception as e:
            print("Connection error:", e)
            await self.shutdown()

    async def message_sender(self):
        while not self.shutdown_event.is_set():
            messages_sent = 0
            while messages_sent < MAX_MESSAGE_PER_SECOND:
                try:
                    message = self.send_queue.get_nowait()
                    await self.websocket.send(message)
                    print(f"Message: {message}")
                    messages_sent += 1
                except asyncio.QueueEmpty:
                    break
            await asyncio.sleep(5)

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                print(f"Message Received {message}")
                try:
                    await send_message('binance_data', 'key', message)
                except Exception as e:
                    print(f"Kafka Error: {e}")
                await asyncio.sleep(3)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed {e}")
        except Exception as e:
            print("Error to receive messages", e)
            await self.shutdown()

    async def subscribe(self, stream):
        if stream in self.current_subscriptions:
            print(f"Already subscribe in: {stream}")
            return
        if len(self.current_subscriptions) >= MAX_STREAMS_PER_CONNECTION:
            print("Limit of Streams")
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

    async def unsubscribe_all(self):
        for stream in list(self.current_subscriptions):
            await self.unsubscriber(stream)

    async def shutdown(self, loop):
        if self.shutdown_event.is_set():
            return
        print("Shutdown...")
        self.shutdown_event.set()
        await self.unsubscribe_all()
        if self.websocket:
            await self.websocket.close()
        loop.stop()
        print("Shutdown completed")


def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams
    client = BinanceWebSocket("wss://stream.binance.com:9443/ws")
    loop.create_task(client.connect())
    loop.create_task(client.subscribe("btcusdt@trade"))

    loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(client.shutdown(loop)))

    try:
        loop.run_forever()
    finally:
        loop.close()
        print("Loop Finished")


if __name__ == '__main__':
    run()
