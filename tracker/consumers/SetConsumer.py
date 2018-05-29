from channels.generic.websocket import WebsocketConsumer
from tracker.models.models import UserProfile
import json
import logging
from tracker.models.models import User
from asgiref.sync import async_to_sync
from django.db import close_old_connections


class SetConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('django')
        WebsocketConsumer.__init__(self, *args, **kwargs)

    def connect(self):
        user = str(self.scope['user'])
        anonymousUser = (user == "AnonymousUser" or user is None)
        self.logger = logging.getLogger('django')
        if not anonymousUser:
            self.accept()
            user = User.objects.get(username=str(self.scope['user']))
            # user_profile = self.__initialize_user__(user.id)
            self.logger.info("Connected to %s, ID: %s" % (user, user.id))
            async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
            print("Connected to %s, ID: %s" % (user, user.id))
        else:
            print("Denied connection to anonymous")
            # login the user to this session.

    def disconnect(self, code):
        self.logger.info("Disconnected from %s" % self.scope['user'])
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        close_old_connections()
        print("Disconnected")

    def receive(self, text_data=None, bytes_data=None):
        self.scope["session"].save()
        if self.__message_valid__(text_data):
            print("Valid %s" % text_data)
            message = json.loads(text_data)
            async_to_sync(self.channel_layer.group_send)("chat", {"type": "chat.message", "text": str(message)})
        else:
            self.send(json.dumps({'message': 'Invalid message. Disconnect.'}))
            self.disconnect(400)

    def chat_message(self, event):
        self.send(text_data=event["text"])

    def __initialize_user__(self, user):
        print("USER: %s" % user)
        profile = UserProfile.objects.get(user=user)
        return profile

    def __message_valid__(self, text_data):
        """
        Checks whether a message has the appropriate format.
        :param message: Message to be checked.
        :return: True if format is OK, False otherwise.
        """
        try:
            message = json.loads(text_data)
            return True
        except Exception as e:
            print(e)
            print("Exception: %s" % text_data)
            return False
