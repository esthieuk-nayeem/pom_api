from rest_framework import serializers
from authentication.models import User
from  .models import Messege


class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = '__all__'

class SubUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','full_name','phone']

class MessegeSerializer(serializers.ModelSerializer):
    user = SubUserSerializer()
    class Meta:
        model = Messege
        fields = ['id','user','text','created_at']

class MessegeSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Messege
        fields = '__all__'


