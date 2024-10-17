
from rest_framework import serializers
from django.contrib.auth import get_user_model

class SignupSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = get_user_model()(

            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
            nickname=validated_data["nickname"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password",
            "email",
            "nickname",
        ]
