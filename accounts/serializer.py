from rest_framework import serializers
from accounts.models import User

class UserSeralizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","password","phone","dob","height","weight"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)