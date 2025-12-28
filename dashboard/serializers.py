from rest_framework import serializers
from .models import RequestQuote


class RequestQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestQuote
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'description', 'created_at']