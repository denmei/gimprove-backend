from channels.generic.websocket import WebsocketConsumer
from tracker.models.models import ClientConnection
from main.models.models import UserProfile
import json
import logging
from tracker.models.models import User
from asgiref.sync import async_to_sync
from django.db import close_old_connections


class SetConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('django')
        self.anonymousUser = True
        WebsocketConsumer.__init__(self, *args, **kwargs)

    def connect(self):
        user = str(self.scope['user'])
        self.anonymousUser = (user == "AnonymousUser" or user is None)
        self.logger = logging.getLogger('django')
        self.accept()
        if not self.anonymousUser:
            print("accepeted. %s" % self.channel_name)
            user = User.objects.get(username=str(self.scope['user']))
            # user_profile = self.__initialize_user__(user.id)
            self.logger.info("Connected to %s, ID: %s" % (user, user.id))
            async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
            if len(UserProfile.objects.filter(user=user)) == 1:
                rfid_tag = UserProfile.objects.get(user=user).rfid_tag
                ClientConnection.objects.all().delete()
                ClientConnection.objects.create(name=self.channel_name, rfid_tag=rfid_tag)
                print("Added channel: %s, %s" % (rfid_tag, self.channel_name))
            self.logger.info("Connected to %s, ID: %s" % (user, user.id))
        else:
            self.disconnect(401)
            self.logger.info("Denied connection to anonymous")

    def disconnect(self, code):
        self.logger.info("Disconnected from %s" % self.scope['user'])
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        if not self.anonymousUser:
            ClientConnection.objects.get(rfid_tag=UserProfile.objects.get(user=self.scope['user']).rfid_tag).delete()
        close_old_connections()
        print("Disconnected")

    def receive(self, text_data=None, bytes_data=None):
        # self.scope["session"].save()
        if self.__message_valid__(text_data):
            message = json.loads(text_data)
            rfid_tag = message['rfid']
            channel_name = ClientConnection.objects.get(rfid_tag=rfid_tag).name
            self.logger.info("Message: %s to %s" % (message, channel_name))
            async_to_sync(self.channel_layer.send)(channel_name, {"type": "chat.message", "text": str(message)})
        else:
            self.logger.info("Invalid request: %s" % text_data)
            self.send(json.dumps({'status_code': '400', 'content': 'Invalid request'}))

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
            valid = True
            message = json.loads(text_data)
            required_keys = ['rfid', 'repetitions', 'weight', 'exercise_name']
            for required_key in required_keys:
                if required_key not in message:
                    valid = False
            return valid
        except Exception as e:
            print(e)
            print("Exception: %s" % text_data)
            return False
