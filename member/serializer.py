
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

# 회원가입용 시리얼라이저
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user


# 로그인용 시리얼라이저
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("잘못된 로그인 정보입니다.")

        if not user.is_active:
            raise serializers.ValidationError("비활성화된 사용자입니다.")

        attrs['user'] = user
        return attrs
