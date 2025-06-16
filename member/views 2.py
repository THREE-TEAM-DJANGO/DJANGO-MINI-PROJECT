from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login as django_login, logout as django_logout, get_user_model, authenticate
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer

from member.serializer import LoginSerializer, UserSignupSerializer, LogoutSerializer, \
    UserListSerializer, PasswordResetSerializer, UsernameFindSerializer

User = get_user_model()
# Create your views here.



class UserListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입 되었습니다"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # form =UserCreationForm(request.POST or None)    # 아래 코드와 같음
    # if form.is_valid():
    #     form.save()
    #     return redirect(settings.LOGIN_URL)
    #
    # context = {
    #     "form": form,
    # }
    # return render(request, "", context)


class TokenObtainView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"message": "로그인 페이지입니다"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            django_login(request, user)
            return Response({"message": "로그인 하였습니다"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # form = AuthenticationForm(request, request.POST or None)
    # if form.is_valid():
    #     django_login(request, form.get_user())
    #
    #     next = request.GET.get()
    #     if next:
    #         return redirect(next)
    #
    #
    #     return redirect(reverse(''))
    #
    # context = {
    #     'form': form
    # }
    # return render(request, '', context)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    #회원 수정
    def patch(self, request):
        serializer = UserListSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    # 회원 삭제
    def delete(self, request):
        request.user.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]  # 또는 IsAuthenticated로 변경 가능


    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "로그아웃 되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
    # form = AuthenticationForm(request, request.POST or None)
    # if form.is_valid():
    #     django_login(request, form.get_user())
    #
    #     next_url = request.GET.get()
    #     if next_url:
    #         return redirect(next_url)
    #
    #     return redirect(reverse(''))
    #
    # context = {
    #     "form": form,
    # }
    #
    # return render(request, '', context)


# 아이디(Username) 찾기
class UsernameFindView(APIView):
    def post(self, request):
        serializer = UsernameFindSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.get_username()
            return Response({"username": username}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 비밀번호 재설정
class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)