from adrf import serializers
from rest_framework import serializers as srl



class RegisterSerializerAsync(serializers.Serializer):
    username = srl.CharField()
    password = srl.CharField()
    email = srl.EmailField()
    cpassword = srl.CharField()
    first_name = srl.CharField()
    last_name = srl.CharField()
    location = srl.JSONField()
    profile_picture = srl.ImageField()
class LoginSerializerAsync(serializers.Serializer):
    username= srl.CharField()
    password = srl.CharField()