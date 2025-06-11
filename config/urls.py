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

from ledger import views as ledger_views
from member import views as member_views



urlpatterns = [
    path("admin/", admin.site.urls),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("users/", ledger_views.user_list, name="user_list"),
    path("account/create/", ledger_views.create_account_view, name="account_create"),
    path("account/<int:pk>", ledger_views.account_list_view, name="account_list"),
    path("signup/", member_views.signup, name="signup"),
    path("login/", member_views.login, name="login"),
    path("logout/", member_views.logout, name="logout"),
    path("transaction/update/<int:pk>", ledger_views.update_transaction, name="update_transaction"),
    path("transaction/delete/<int:pk>", ledger_views.delete_transaction, name="delete_transaction"),
]
