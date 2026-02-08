from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "avatar", "date_joined")
        
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=50)
    last_name  = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True, max_length=8)
    password2 = serializers.CharField(write_only=True, max_length=8)
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        
        user = User.objects.create_user(password=password, **validated_data)
        
        refresh = RefreshToken.for_user(user)
        
        return {
            "user": UserSerializer(user).data,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }