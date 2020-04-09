from rest_framework import serializers
from accounts.models import *



class dataSerializer(serializers.ModelSerializer):
    # keystore = serializers.CharField()
    # key = serializers.CharField()
    class Meta:
        model = temp
        fields=('keystore','keystore_pass', 'key', 'key_pass',)