from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import LocationProfile
from django.http.response import JsonResponse
from profiles.models import Profile
from django.contrib.gis.geos.point import Point



@csrf_exempt
def get_user_location(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        new_location = LocationProfile.objects.update_or_create(user=user, latitude=latitude, longitude=longitude)
        # user_data = dict()
        user_profile: Profile = user.profile
        user_data = {
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'gender': user_profile.gender,
            'profile_picture': user_profile.profile_main_picture.image.url,
            'profile_url': user_profile.get_absolute_url(),
        }

        return JsonResponse(user_data)
    return JsonResponse({'message': 'error'})


def map_view(request):
    context = dict()

    return render(request, template_name='map/map.html')



# Create your views here.
