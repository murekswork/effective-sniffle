from .models import Notification


def create_match_notification(sender_profile, receiver_profile):
    notification = Notification(recipient=sender_profile, additional_profile=receiver_profile, type='match')
    notification.message = notification.create_new_match_notification_text()
    notification.save()