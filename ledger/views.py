import json

from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ledger.models import Account, Transaction
from ledger.serializer import AccountSerializer, TransactionSerializer

# Create your views here.

User = get_user_model()




# 계좌 생성
class AccountCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        serializer = AccountSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            account = serializer.save()
            return Response(
                {
                    "message": "계좌가 생성되었습니다",
                    "account_number": account.account_number
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # if request.method == "POST":
    #
    #     user_id = request.GET.get('user_id')
    #     account_number = request.GET.get('account_number')
    #     initial_balance = request.GET.get('initial_balance')
    #
        # user = get_object_or_404(User, pk=pk)
    #
    #     account = Account.objects.create(
    #         user=user,
    #         account_number=account_number,
    #         initial_balance=initial_balance,
    #         balance=initial_balance,
    #     )
    #     return JsonResponse({"message": "계좌가 생성되었습니다", "account_number": account.account_number})

    # data = request.data.copy()
    # data["user"] = request.user.id


# 계좌 리스트 조회
class AccountListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


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

class AccountDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            account = Account.objects.get(pk=pk, user=request.user)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        account.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class TransactionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.validated_data['account']
            if account.user != request.user:
                return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account_id = request.GET.get('account')
        ts_type = request.GET.get('type')
        min_amount = request.GET.get('min_amount')

        queryset = Transaction.objects.filter(account__user=request.user)

        if account_id:
            queryset = queryset.filter(account_id=account_id)
        if ts_type:
            queryset = queryset.filter(type=ts_type)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)



# 거래 수정
class TransactionUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, pk):
        return self.update(request, pk)

    def update(self, request, pk):
        transaction = get_object_or_404(Account, pk=pk)
        serializer = TransactionSerializer(transaction, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import json

from django.contrib.auth import get_user_model, authenticate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from ledger.models import Account, Transaction
from ledger.serializer import AccountSerializer, TransactionSerializer

# Create your views here.

User = get_user_model()




# 계좌 생성
class AccountCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        serializer = AccountSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            account = serializer.save()
            return Response(
                {
                    "message": "계좌가 생성되었습니다",
                    "account_number": account.account_number
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # if request.method == "POST":
    #
    #     user_id = request.GET.get('user_id')
    #     account_number = request.GET.get('account_number')
    #     initial_balance = request.GET.get('initial_balance')
    #
        # user = get_object_or_404(User, pk=pk)
    #
    #     account = Account.objects.create(
    #         user=user,
    #         account_number=account_number,
    #         initial_balance=initial_balance,
    #         balance=initial_balance,
    #     )
    #     return JsonResponse({"message": "계좌가 생성되었습니다", "account_number": account.account_number})

    # data = request.data.copy()
    # data["user"] = request.user.id


# 계좌 리스트 조회
class AccountListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


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

class AccountDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            account = Account.objects.get(pk=pk, user=request.user)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        account.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class TransactionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.validated_data['account']
            if account.user != request.user:
                return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        account_id = request.GET.get('account')
        ts_type = request.GET.get('type')
        min_amount = request.GET.get('min_amount')

        queryset = Transaction.objects.filter(account__user=request.user)

        if account_id:
            queryset = queryset.filter(account_id=account_id)
        if ts_type:
            queryset = queryset.filter(type=ts_type)
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)

        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)



# 거래 수정
class TransactionUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, pk):
        return self.update(request, pk)

    def update(self, request, pk):
        transaction = get_object_or_404(Account, pk=pk)
        serializer = TransactionSerializer(transaction, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 거래 삭제
class TransactionDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, pk):
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


