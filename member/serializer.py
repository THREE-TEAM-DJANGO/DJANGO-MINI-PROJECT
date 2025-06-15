
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# 사용자 전체 목록 조회
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "is_active", "is_admin"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


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


class TokenObtainSerializer(serializers.Serializer):
    # permission_classes = [AllowAny]
    # serializer_class = TokenObtainPairSerializer

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('잘못돤 사용자 또눈 바밀번호압나더')

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'user_id': user.id
        }


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

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            self.fail('bad_token')

# username 찾기
class UsernameFindSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("해당 이메일로 가입된 사용자가 없습니다.")
        return value

    def get_username(self):
        user = User.objects.get(email=self.validated_data['email'])
        return user.username


# 비밀번호 재설정용
class PasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("존재하지 않는 사용자입니다.")
        return data

    def save(self):
        user = User.objects.get(username=self.validated_data['username'])
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user