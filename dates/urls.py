from django.urls import path, include

from dates.views import PublicPageView

urlpatterns = [
    path('dates/public/', PublicPageView.as_view(), name='public'),
]