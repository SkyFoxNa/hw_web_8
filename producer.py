from faker import Faker
from models import Contact

# Підключення
from conects import connect, channel, connection

# Параметри RabbitMQ
channel.queue_declare(queue='contacts')

# Оголошення черг для SMS та електронної пошти
channel.queue_declare(queue='sms_contacts')
channel.queue_declare(queue='email_contacts')


# Генерування фейкових контактів і збереження у базу даних
def create_fake_contacts(num_contacts):
    fake = Faker('uk_UA')
    for count in range(num_contacts):
        fullname = fake.name()
        email = fake.email()
        phone_number = fake.phone_number()
        contact = Contact(fullname=fullname, email=email, phone_number=phone_number)
        #  Зберігаємо контакт
        contact.save()

        if count % 2 == 0:
            # Розсилка email
            channel.basic_publish(exchange='', routing_key='email_contacts', body=str(contact.id))
        else:
            # Розсилка phone
            channel.basic_publish(exchange='', routing_key='sms_contacts', body=str(contact.id))
        print(f"Додано контакт: {fullname}, {email}, {phone_number}")


if __name__ == "__main__":
    num_contacts = 100
    create_fake_contacts(num_contacts)
    connection.close()
