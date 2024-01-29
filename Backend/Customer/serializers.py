from rest_framework import serializers
from .models import Customer,Contact


class CustomerSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    def get_photo_url(self, obj):
        if obj.photo:
            return obj.photo.url
        return None

    class Meta:
        model = Customer
        # fields = '__all__'
        fields = ['id', 'name', 'address', 'city', 'state', 'zip_code', 'country', 'photo','photo_url']

        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contact
        # fields='__all__'
        fields = ['id', 'customer_id', 'email', 'mobile']
