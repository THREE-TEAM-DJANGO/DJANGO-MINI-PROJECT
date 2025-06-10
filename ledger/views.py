import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ledger.models import Account
from ledger.serializer import UserSerializer, AccountSerializer, TransactionSerializer

# Create your views here.

User = get_user_model()

# 사용자 전체 목록 조회
@api_view(["GET"])
def user_list(request):
    # users = User.objects.all()
    # context = {"users": users}
    # return render(request, "", context)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# 계좌 생성
@api_view(["POST"])
def create_account_view(request):
    # if request.method == "POST":
    #
    #     user_id = request.GET.get('user_id')
    #     account_number = request.GET.get('account_number')
    #     initial_balance = request.GET.get('initial_balance')
    #
    #     user = get_object_or_404(User, id=user_id)
    #
    #     account = Account.objects.create(
    #         user=user,
    #         account_number=account_number,
    #         initial_balance=initial_balance,
    #         balance=initial_balance,
    #     )
    #     return JsonResponse({"message": "계좌가 생성되었습니다", "account_number": account.account_number})

    serializer = AccountSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        return Response({"message": "계좌가 생성되었습니다", "account_number": account.account_number}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 계좌 리스트 조회
@api_view(["GET"])
def account_list_view(request, user_id):
    # accounts = Account.objects.filter(user_id=user_id)
    #
    # account_data = []
    # for account in accounts:
    #     account_data = ({
    #     "users":account.user.name,
    #     "account_number": account.account_number,
    #     "balance": account.balance,
    #     "created_at": account.created_at.strftime("%Y-%m-%d %H:%M:%S"),
    #     })

    accounts = Account.objects.filter(user_id=user_id)
    serializer = AccountSerializer(accounts, many=True)
    return Response(serializer.data)



# 거래 수정
@api_view(["PUT, PATCH"])
def update_transaction(request, pk):
    transaction = get_object_or_404(Account, pk=pk)
    serializer = TransactionSerializer(transaction, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 거래 삭제
@api_view(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Account, pk=pk)
    transaction.delete()
    return Response({"message": "삭제 완료"}, status=status.HTTP_204_NO_CONTENT)





# #계좌 삭제
# def delete_account_view(request, pk):
#     try:
#         account = Account.objects.get(pk=pk)
#     except Account.DoesNotExist:
#         return JsonResponse({"error": "계좌가 존재하지 않습니다."}, status=404)
#
#     if account.user != request.user:
#         return JsonResponse({"error": "권한이 없습니다."}, status=403)
#
#     account.delete()
#     return JsonResponse({"message": "계좌가 삭제되었습니다."})

