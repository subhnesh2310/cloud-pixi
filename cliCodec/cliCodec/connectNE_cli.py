from google.cloud import pubsub_v1
from paramiko import SSHClient, AutoAddPolicy
import json
import os
from django.http import JsonResponse, HttpResponse
from concurrent.futures import TimeoutError
from django.views.decorators.csrf import csrf_exempt
from cliCodec.g40 import connectNE

message_data = None

def callback(message):
    global message_data
    message_data = message.data
    message.ack()

# def callback(message):
#     import ipdb; ipdb.set_trace()
#     try:
#         global message_data
#         message_data = message.data
#         # username = message_data.get('username')
#         # password = message_data.get('password')
#         # hostname = message_data.get('hostname')
#         # port_number = message_data.get('port_number')
#         # interface = message_data.get('interface')
#         # handle = message_data.get('handle')

#         # Perform business logic
#         # result = execute_ssh_command(username, password, hostname, port_number, interface, handle)
       
#         result = message_data

#         # # Publish response
#         publish_response(result)

#         print(message_data)
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


def subscribe_to_request_topic(project_id, subscription_name):
    global message_data
    try:
        # import ipdb; ipdb.set_trace()
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

# @csrf_exempt  
def connectNE_subscription(request):
    global message_data
    project_id = 'cloud-pixi'
    subscription_name = 'projects/cloud-pixi/subscriptions/connect_NE_Sub'

    try:
        subscribe_to_request_topic(project_id, subscription_name)
        import ipdb; ipdb.set_trace()
        # Check if message data is available
        if message_data:
            data = message_data.decode("utf-8")
            result_data = json.loads(data)
            user = result_data.get('username')
            pw = result_data.get('password')
            ip = result_data.get('hostname')
            # port_number = result_data.get('port_number')
            interface = result_data.get('interface')
            handle = result_data.get('handle')

            #Perform business logic
            result = connectNE(handle, ip, user, pw, interface=interface)

            print(result)
            #Publish response
            publish_response(result)
            return JsonResponse({'message_data': result.decode("utf-8")})
        else:
            return JsonResponse({'message': 'No data received from Pub/Sub.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def publish_response(result):
    import ipdb; ipdb.set_trace()
    try:
        # import ipdb; ipdb.set_trace()
        publisher = pubsub_v1.PublisherClient()
        topic_path = 'projects/cloud-pixi/topics/connectNE_Response'

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
        print("Response published Successfully")
    except Exception as e:
        print("Error publishing response:", e)