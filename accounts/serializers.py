from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["id", "email", "password", "role"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "role"]

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    # accept email instead of username
    username_field = "email"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add custom claims
        token["role"] = user.role
        token["email"] = user.email
        return token

    def validate(self, attrs):
        # attrs contains "email" by default due to username_field
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "role": self.user.role,
        }
        return data
