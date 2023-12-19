from django.urls import path, include
from .views import CustomSignupView

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/signup/', CustomSignupView.as_view(), name='custom_account_signup')
]