"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from ledger.views import (
                                   AccountCreateView,
                                   AccountDeleteView,
                                   AccountListView,
                                   TransactionCreateView,
                                   TransactionDeleteView,
                                   TransactionListView,
                                   TransactionUpdateView,
)
from member.views import (
    LogoutView,
    PasswordResetView,
    SignUpView,
    UserDeleteView,
    UserListView,
    UsernameFindView,
    UserUpdateView,
    LoginAndTokenView,
    TokenRefreshAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('api/login/', LoginAndTokenView.as_view(), name='login-and-token'),
    path('api/token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path("api/token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/user/", UserListView.as_view(), name="user_list"),
    path("api/user/update/<int:pk>/", UserUpdateView.as_view(), name="user-update"),
    path("api/user/delete/<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
    path("api/find-username/", UsernameFindView.as_view(), name="find-username"),
    path("api/reset-password/", PasswordResetView.as_view(), name="reset-password"),
    path("api/account/", AccountListView.as_view(), name="account_list"),
    path("api/account/create/", AccountCreateView.as_view(), name="account_create"),
    path("api/account/delete/<int:pk>/", AccountDeleteView.as_view()),
    path("api/transactions/", TransactionListView.as_view()),
    path("api/transactions/create/", TransactionCreateView.as_view()),
    path("api/transaction/update/<int:pk>/", TransactionUpdateView.as_view, name="update_transaction",),
    path(
        "api/transaction/delete/<int:pk>/",
        TransactionDeleteView.as_view,
        name="delete_transaction",
    ),
]
