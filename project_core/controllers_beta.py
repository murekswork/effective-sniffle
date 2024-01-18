from typing import List

from profiles.models import Notification, Profile
from chats.models import Message, Chat
from like.models import Match, LikeModel
from moderating.models import Complain


class NotificationControllerMixin:


    @staticmethod
    def message_send_notification(message: Message) -> Notification:
        message_notification = Notification.objects.create(message=f'You have new message from {message.receiver}!',
                                                           recipient=message.receiver,
                                                           type='message_notification',
                                                           additional_profile=message.sender)
        message_notification.save()
        return message_notification

    @staticmethod
    def match_notification(sender: Profile, match: Match) -> Notification:
        if sender == match.profile1:
            recipient = match.profile2
        else:
            recipient = match.profile1
        notification_for_receiver = Notification.objects.create(message=f'You have a new match with {sender} now you write messages each other!',
                                                   recipient=recipient,
                                                   type='match_notification',
                                                   additional_profile=sender)
        notification_for_receiver.save()
        notification_for_sender = Notification.objects.create(message=f'You have a new match with {recipient} now you write messages each other!',
                                                   recipient=sender,
                                                   type='match_notification',
                                                   additional_profile=recipient)
        notification_for_sender.save()
        return notification_for_sender

    @staticmethod
    def complain_notification(complain: Complain) -> Notification:
        notification = Notification.objects.create(message=f'We get your complain! Our moderating command will check '
                                                                   f'{complain.receiver} and take appropriate measures!',
                                                           recipient=complain.sender,
                                                           type='complain_notification',
                                                           additional_profile=complain.receiver
                                                           )

        return notification

    @staticmethod
    def like_notification(like: LikeModel) -> Notification:
        notification = Notification.objects.create(message=f'{like.sender} liked you!',
                                                   recipient=like.receiver,
                                                   type='like_notification',
                                                   additional_profile=like.sender)
        return notification

    @staticmethod
    def read_all_notifications(notifications: List[Notification]) -> List[Notification]:
        return notifications.update(read_status=True)



class MatchController(NotificationControllerMixin):

    def create_match(self, profile1, profile2):
        match = Match.objects.create(profile1=profile1, profile2=profile2)
        match.save()
        chat = Chat.objects.create(match=match)
        chat.profiles.add(profile1, profile2)
        chat.save()
        notification = self.match_notification(profile1, match)
        return match


class LikeControllerMixin(NotificationControllerMixin):

    def like(self, receiver, sender):
        like = LikeModel.objects.create(receiver=receiver, sender=sender)
        match_check = self.check_if_like_creates_match(like)
        self.like_notification(like)
        return like

    def check_existing_like(self, receiver, sender):
        pass

    def delete_like(self, like: LikeModel):
        return like.delete()

    def check_if_like_creates_match(self, like: LikeModel):
        second_like = LikeModel.objects.filter(sender=like.receiver, receiver=like.sender).first()
        if second_like:
            match = MatchController().create_match(profile1=like.sender, profile2=like.receiver)
        return second_like


