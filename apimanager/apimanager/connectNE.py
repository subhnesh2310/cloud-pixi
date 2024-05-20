import json
import requests
import ipdb
import os
import time
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from google.cloud import pubsub_v1
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apimanager.serializers import ConnectNESerializers
from paramiko import SSHClient, AutoAddPolicy
from rest_framework.exceptions import ParseError
from concurrent.futures import TimeoutError

@method_decorator(csrf_exempt, name='dispatch')
class ConnectView(APIView):
    message_data = None
    def post(self, request):
        # import ipdb; ipdb.set_trace()
        data = request.data
        username = data.get('username')
        password = data.get('password')
        hostname = data.get('hostname')
        port_number = data.get('port')
        interface = data.get('interface')
        handle = data.get('handle')
        serializer = ConnectNESerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save data to the database
            print("---------------------------->", data)
            # Publish parameters to Pub/Sub topic
            try:
                key_path = 'C://Users//subkumar//Desktop//CloudPixi//apimanager//apimanager//token_key.json'
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
                publisher = pubsub_v1.PublisherClient()
                topic_path = 'projects/cloud-pixi/topics/connect_NE'
                message_data = json.dumps({
                    'username': username,
                    'password': password,
                    'hostname': hostname,
                    'port_number': port_number,
                    'interface': interface,
                    'handle':handle
                }).encode('utf-8')
                future = publisher.publish(topic_path, data=message_data)
                future.result()
                print("Request Publish Successfully")
                
                # Flag to indicate successful publishing
                published_successfully = True

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        
        else:
            return JsonResponse({'error': serializer.errors}, status=400)

        # If data is published successfully, call the Subscriber API
        if published_successfully:
            try:
                # Calling Subscriber API to subscribe data and push into another response topic
                response = requests.get("http://127.0.0.1:8001/api/connectNE_subscription/")
                print(f"---->Response will be : {response.text}")

            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

            # Subscribe to response topic
            time.sleep(60)
            result = self.connectNE_response_subscription()
            # Assuming result is a JSON string
            result_json_str = result.decode("utf-8")
            print(f"Result will be : {result_json_str}, {type(result_json_str)}")
            
            return JsonResponse(json.loads(result.decode("utf-8")))
        
        else:
            return JsonResponse({'error': serializer.errors}, status=400)
    

    def callback(self, message):
        global message_data
        message_data = message.data
        message.ack()

    def subscribe_to_response_topic(self, project_id, subscription_name):
        global message_data
        try:
            # import ipdb; ipdb.set_trace()
            key_path = 'C://Users//subkumar//Desktop//CloudPixi//apimanager//apimanager//token_key.json'
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path
            timeout=10.0
            subscriber = pubsub_v1.SubscriberClient()
            subscription_path = subscription_name
            publisher_result = subscriber.subscribe(subscription_path, callback=self.callback)
            print(f"Subscribed to request topic: {publisher_result}")
        except Exception as e:
            print("Error subscribing to request topic:", e)

        with subscriber:
            try:
                publisher_result.result(timeout=timeout)
            except TimeoutError:
                publisher_result.cancel()
                publisher_result.result()

    def connectNE_response_subscription(self):
        # import ipdb; ipdb.set_trace()
        global message_data
        project_id = 'cloud-pixi'
        subscription_name = 'projects/cloud-pixi/subscriptions/connectNE_Response_Sub'

        try:
            self.subscribe_to_response_topic(project_id, subscription_name)
            # Check if message data is available
            if message_data:
                return message_data
            else:
                return JsonResponse({'message': 'No data received from Pub/Sub.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)