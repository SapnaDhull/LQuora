# serializers.py
from rest_framework import serializers

class InputTextSerializer(serializers.Serializer):
    input_text = serializers.CharField(max_length=500)  # Adjust max length as needed
