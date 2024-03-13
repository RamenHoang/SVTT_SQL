import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('10.10.1.23'))
channel = connection.channel()

channel.queue_declare(queue='test_queue')
channel.basic_publish(exchange='', routing_key='test_queue', body='Hello, RabbitMQ!!!')

print(" [x] Sent 'Hello, RabbitMQ!'")

connection.close()
