from django.urls import path, include 
from .views import ComplainPageView, ModeratorsControlPageView, AjaxSendComplainView, ModeratorPageView

urlpatterns = [
	path('complain/<int:pk>/', ComplainPageView.as_view(), name='complain'),
	path('complain/send/', AjaxSendComplainView.as_view(), name='ajax-send-complain'),
	path('', ModeratorPageView.as_view(), name='moderator_page'),
	path('control/', ModeratorsControlPageView.as_view(), name='moderators_control_page'),

]
