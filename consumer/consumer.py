import pika
import base64
import logging
from kubernetes import client, config

# Logging
logging.basicConfig(level=logging.INFO)

#Cluster Config
config.load_incluster_config()

# Take creds droem secrets
def get_secret(namespace, secret_name, key):
    v1 = client.CoreV1Api()
    secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
    encoded_value = secret.data[key].strip()
    decoded_value = base64.b64decode(encoded_value).decode('utf-8')
    return decoded_value

#callback
def callback(ch, method, properties, body):
    logging.info(f"Received message: {body}")
    print(f"Received message: {body}")


# Secret Data
namespace = 'rabbitmq'
secret_name = 'rabbitmq-test-credentials'
rabbitmq_user_key = 'auth.username'
rabbitmq_password_key = 'auth.userpassword'

rabbitmq_user_key = get_secret(namespace, secret_name, rabbitmq_user_key).strip()
rabbitmq_password_key = get_secret(namespace, secret_name, rabbitmq_password_key).strip()

#print(rabbitmq_user_key)
#print(rabbitmq_password_key)

# Data needed for connection
hostname = 'rabbitmq-headless.rabbitmq.svc.cluster.local'
port = 5672
virtual_host = '/'
queue_name = 'test1'

print(f"Username: {rabbitmq_user_key}")
print(f"Password: {rabbitmq_password_key}")

# Creating connection
credentials = pika.PlainCredentials(rabbitmq_user_key, rabbitmq_password_key)
parameters = pika.ConnectionParameters(hostname, port, virtual_host, credentials)
connection = pika.BlockingConnection(parameters)

try:
    # Connection to chanel
    channel = connection.channel()

    print("Logged in RabbitMQ")
    channel.queue_declare(queue='test1', durable=True)
    channel.basic_consume(queue='test1', on_message_callback=callback, auto_ack=True)

    # Start lisening
    print('Waiting for messages for finish press CTRL+C')
    channel.start_consuming()

except KeyboardInterrupt:
    print("Interupted by user")

finally:
    # Closing connection
    connection.close()









