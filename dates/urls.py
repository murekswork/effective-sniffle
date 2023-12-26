from django.urls import path, include

from dates.views import PublicPageView, MeetsPageView

urlpatterns = [
    path('dates/public/', PublicPageView.as_view(), name='public'),
    path('dates/meets/', MeetsPageView.as_view(), name='meets'),
]