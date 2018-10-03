from channels.generic.websocket import WebsocketConsumer
from app_tracker.models.models import ClientConnection
from app_main.models.models import UserProfile
import json
import logging
from app_tracker.models.models import User, Equipment
from asgiref.sync import async_to_sync
from django.db import close_old_connections


class SetConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('django')
        self.anonymousUser = True
        WebsocketConsumer.__init__(self, *args, **kwargs)

    def connect(self):
        """
        Creates a new connection between a client and the server. For each connection, a new instance of the
        ClientConnection-model is created. This allows to query the connection later on.
        :return:
        """
        user = str(self.scope['user'])
        self.anonymousUser = (user == "AnonymousUser" or user is None)
        self.logger = logging.getLogger('django')
        self.accept()
        if not self.anonymousUser:
            print("accepted. %s" % self.channel_name)
            user = User.objects.get(username=str(self.scope['user']))
            # user_profile = self.__initialize_user__(user.id)
            self.logger.info("Connected to %s, ID: %s" % (user, user.id))
            async_to_sync(self.channel_layer.group_add)("chat", self.channel_name)
            ClientConnection.objects.filter(user=user).delete()
            ClientConnection.objects.create(name=self.channel_name, user=user)
            print("Added channel: %s, %s" % (user, self.channel_name))
            self.logger.info("Connected to %s, ID: %s" % (user, user.id))
        else:
            print("not accepted")
            self.disconnect(401)
            self.logger.info("Denied connection to anonymous")

    def disconnect(self, code):
        self.logger.info("Disconnected from %s" % self.scope['user'])
        async_to_sync(self.channel_layer.group_discard)("chat", self.channel_name)
        if not self.anonymousUser:
            ClientConnection.objects.get(user=UserProfile.objects.get(user=self.scope['user'])).delete()
        close_old_connections()
        print("Disconnected")

    def receive(self, text_data=None, bytes_data=None):
        # self.scope["session"].save()
        if self.__message_valid__(text_data):
            message = json.loads(text_data)
            rfid = message['rfid']
            user = UserProfile.objects.get(rfid_tag=rfid)
            channel_name = ClientConnection.objects.get(user=user).name
            print("Forwarding to %s" % channel_name)
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
            required_keys = ['rfid', 'repetitions', 'weight', 'exercise']
            for required_key in required_keys:
                if required_key not in message:
                    valid = False
            return valid
        except Exception as e:
            print(e)
            print("Exception: %s" % text_data)
            return False
