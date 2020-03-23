from rest_framework import serializers

class dataSerializer(serializers.Serializer):
    keystore = serializers.CharField()
    key = serializers.CharField()