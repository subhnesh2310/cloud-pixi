from rest_framework import serializers
from apimanager.models import ConnectNE
from apimanager.models import SendRCV
from apimanager.models import DiconnectNE

class ConnectNESerializers(serializers.ModelSerializer):
    class Meta:
        model = ConnectNE
        fields = '__all__'

class DisconnectNESerializers(serializers.ModelSerializer):
    class Meta:
        model = DiconnectNE
        fields = '__all__'

class SendRCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendRCV
        fields = '__all__'