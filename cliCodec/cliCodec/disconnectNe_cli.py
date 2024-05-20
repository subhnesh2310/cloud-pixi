from google.cloud import pubsub_v1
from paramiko import SSHClient, AutoAddPolicy
import json
import os
from django.http import JsonResponse
from concurrent.futures import TimeoutError

message_data = None
def callback(message):
    global message_data
    message_data = message.data
    message.ack()

# def callback(message):
#     try:
#         import ipdb; ipdb.set_trace()
#         data = json.loads(message.data.decode("utf-8"))
#         username = data.get('username')
#         password = data.get('password')
#         hostname = data.get('hostname')
#         port_number = data.get('port_number')
#         interface = data.get('interface')
#         handle = data.get('handle')

#         # Perform business logic
#         # result = execute_ssh_command(username, password, hostname, port_number, interface, handle)
#         result = data
        
#         # # Publish response
#         # publish_response(result)
#         print(data)
#         message.ack()  # Acknowledge the message
        
    # except Exception as e:
    #     print("Error handling message:", e)

def execute_ssh_command(username, password, hostname, port_number, interface, handle):
    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(hostname, port=port_number, username=username, password=password)
        stdin, stdout, stderr = ssh.exec_command(handle)
        result = stdout.read().decode().strip()
        ssh.close()
        print("SSH connection result:", result)
        return result
    except Exception as e:
        print("Error executing SSH command:", e)

def publish_response(result):
    try:
        # import ipdb; ipdb.set_trace()
        publisher = pubsub_v1.PublisherClient()
        topic_path = 'projects/cloud-pixi/topics/disconnectNE_Res'

        # Decode the binary data into a string
        result_str = result.decode('utf-8')

        # Parse the string as JSON
        result_json = json.loads(result_str)

        # Encode the JSON data to bytes
        message_data = json.dumps({
            'response': result_json
        }).encode('utf-8')

        future = publisher.publish(topic_path, data=message_data)
        future.result()
    except Exception as e:
        print("Error publishing response:", e)


def subscribe_to_request_topic(project_id, subscription_name):
    global message_data
    try:
        key_path = 'C://Users//subkumar//Desktop//CloudPixi//cliCodec//cliCodec//token_key.json'
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
        timeout=5.0
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscription_name
        publisher_result = subscriber.subscribe(subscription_path, callback=callback)
        print(f"Subscribed to request topic: {publisher_result}")
    except Exception as e:
        print("Error subscribing to request topic:", e)

    with subscriber:
        try:
            publisher_result.result(timeout=timeout)
        except TimeoutError:
            publisher_result.cancel()
            publisher_result.result()
    
def disconnectNE_subscription(request):
    global message_data
    project_id = 'cloud-pixi'
    subscription_name = 'projects/cloud-pixi/subscriptions/disconnectNE_Req'
    try:
        subscribe_to_request_topic(project_id, subscription_name)
        if message_data:
            publish_response(message_data)
            return JsonResponse({'message_data': message_data.decode("utf-8")})
        else:
            return JsonResponse({'message': 'No data received from Pub/Sub.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)