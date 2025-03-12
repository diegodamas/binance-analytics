from confluent_kafka import Producer  # type: ignore[import]

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'client.id': 'binance_data',
    'acks': 'all'
})


async def send_message(topic, key, value):

    def delivery_report(err, msg):
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to [{msg.partition()}] at offset {msg.offset()}')

    try:
        print("Producing Message")
        producer.produce(topic, key=key, value=value, callback=delivery_report)
    except BufferError as b:
        print(f'BufferError encountered: {b} - Local producer queue is full' f'({len(producer)} messages awaiting delivery)')
        producer.poll(1.0)
    except Exception as e:
        print(f"An unexpected error occurred while producing the message {e}")
        raise

    producer.flush()
    return
