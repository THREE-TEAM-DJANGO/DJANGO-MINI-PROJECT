from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ledger.serializer import UserSerializer
from member.serializer import LoginSerializer


# Create your views here.

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):

    serializer = UserSerializer(data=request.data)
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




@api_view(["GET","POST"])
@permission_classes([AllowAny])
def login(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            django_login(request, user)
            return Response({"message": "로그인 하였습니다"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "로그인 페이지입니다"}, status=status.HTTP_200_OK)

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


@api_view(['POST'])
@permission_classes([AllowAny])
def logout(request):
    django_logout(request)
    return Response({"message": "로그아웃 하였습니다"}, status=status.HTTP_200_OK)


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

