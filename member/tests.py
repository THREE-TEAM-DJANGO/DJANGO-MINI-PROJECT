from django.test import TestCase
from member.serializer import UserSignupSerializer, UserListSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# 회원가입 테스트 코드
class UserSignupSerializerTest(TestCase):
    def test_valid_signup(self):
        data = {
            "username": "testuser",
            "phone_number": "0123456789",
            "password": "telephone12"
        }
        serializer = UserSignupSerializer(data=data)

        # 데이터 유효성 검사
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)

        # 실제 저장 → user 생성
        user = serializer.save()

        # DB에 저장된 값 비교
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.phone_number, data['phone_number'])

        # 비밀번호가 암호화되었는지 확인
        self.assertTrue(user.check_password(data['password']))

    def test_signup_missing_fields(self):
        data = {
            "username": "testuser",
        }
        serializer = UserSignupSerializer(data=data)

        # 필드 누락 시 is_valid는 False
        self.assertFalse(serializer.is_valid())
        self.assertIn("phone_number", serializer.errors)
        self.assertIn("password", serializer.errors)


# 사용자 조회 테스트 코드
class UserListSerializerTest(TestCase):
    def test_user_list_output(self):
        user = User.objects.create_user(
            username="simpleuser",
            phone_number="0123456789",
            password="userpass123"
        )

        serializer = UserListSerializer(user)
        data = serializer.data

        # 출력 데이터에 username 포함
        self.assertEqual(data['username'], "simpleuser")

        # password는 write_only → 출력에 없음
        self.assertNotIn("password", data)

        # 추가 필드 확인
        self.assertIn("is_active", data)
        self.assertIn("is_admin", data)




# Create your tests here.
