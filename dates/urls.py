from django.urls import path, include
from dates.views import PublicPageView, MeetsPageView, ajax_get_profile

urlpatterns = [
    path('dates/public/', PublicPageView.as_view(), name='public'),
    path('dates/meets/', MeetsPageView.as_view(), name='meets'),
    path('ajax-get-profile', ajax_get_profile, name='ajax-get-profile'),
]