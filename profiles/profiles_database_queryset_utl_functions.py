from profiles.models import Profile
from django.db.models import Q


def get_filtered_profiles(request_profile):

        filtered_by_gender_and_orientation_profile_set = Profile.objects.filter(Q(gender=request_profile.orientation) &
                                                                                Q(orientation=request_profile.gender) & Q(user__is_active=True))
        filtered_disliked_profiles = filtered_by_gender_and_orientation_profile_set.exclude(user__id__in=request_profile.get_disliked_profiles())

        filtered_liked_profiles = filtered_disliked_profiles.exclude(user__id__in=request_profile.get_liked_profiles())

        final_filtered_profile_set = filtered_liked_profiles.exclude(user__id__in=request_profile.get_who_disliked_profiles())


        return final_filtered_profile_set
