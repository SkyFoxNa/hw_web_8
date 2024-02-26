import pika
from mongoengine import connect

connect(
    db = "hw_web_8",
    host = "mongodb+srv://user_goit_web:user_goit_web@mains-db.nfj7rrz.mongodb.net/?retryWrites=true&w=majority"
           "&appName=Mains-db",
)


# Параметри RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
