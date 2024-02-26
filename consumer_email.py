from models import Contact

# Підключення
from conects import connect, channel

# Підключення до RabbitMQ
channel.queue_declare(queue='email_contacts')


# Отримання та обробка повідомлень з черги RabbitMQ для email
def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()
    if contact:
        send_email(contact)
        # Позначення, що повідомлення надіслано
        contact.message_sent = True
        contact.save()
        print(f"Відправлено емейл для контакту: {contact.fullname}, {contact.email}")
    else:
        print(f"Контакт з ID {contact_id} не знайдено")


# Виклик функції-заглушки для відправлення емейлу
def send_email(contact):
    # Функція-заглушка, що імітує відправлення емейлу
    print(f"Відправлення емейлу на адресу: {contact.email}")


if __name__ == "__main__":
    channel.basic_consume(queue='email_contacts', on_message_callback=callback, auto_ack=True)
    print("Очікування повідомлень з черги RabbitMQ для email...")
    channel.start_consuming()
