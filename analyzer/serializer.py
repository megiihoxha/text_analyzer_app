from rest_framework import serializers
from django.contrib.auth.models import User

from analyzer.models import AnalysisLog


class TextSerializer(serializers.Serializer):
    text = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

# analyzer/serializers.py


class AnalysisLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisLog
        fields = ['input_text', 'result', 'timestamp']
