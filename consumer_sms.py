from models import Contact

# Підключення
from conects import connect, channel

# Підключення до RabbitMQ
channel.queue_declare(queue='sms_contacts')


# Отримання та обробка повідомлень з черги RabbitMQ для SMS
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_sms(contact)
        # Позначення, що повідомлення надіслано
        contact.message_sent = True
        contact.save()
        print(f"Відправлено SMS для контакту: {contact.fullname}, {contact.phone_number}")
    else:
        print(f"Контакт з ID {contact_id} не знайдено")


# Виклик функції-заглушки для відправлення SMS
def send_sms(contact):
    # Функція-заглушка, що імітує відправлення SMS
    print(f"Відправлення SMS на номер: {contact.phone_number}")


if __name__ == "__main__":
    channel.basic_consume(queue='sms_contacts', on_message_callback=callback, auto_ack=True)
    print("Очікування повідомлень з черги RabbitMQ для SMS...")
    channel.start_consuming()
