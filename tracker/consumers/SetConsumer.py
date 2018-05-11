from channels.generic.websocket import WebsocketConsumer
from tracker.models.models import UserProfile
import json
import logging


class SetConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.user = str(self.scope['user'])
        print(self.user)
        self.anonymousUser = (self.user == "AnonymousUser" or self.user is None)
        logger = logging.getLogger('django')
        logger.info("Connected to %s" % str(self.user))
        """
        if not self.anonymousUser:
            self.user_profile = self.__initialize_user__(self.user)
        self.send("Anonymous User: " + str(self.anonymousUser))"""

    def disconnect(self, code):
        logger = logging.getLogger('django')
        logger.info("Disconnected from %s" % str(self.user))
        print("Disconnected")

    def receive(self, text_data=None, bytes_data=None):
        if self.__message_valid__(text_data) and not self.anonymousUser:
            print("Valid")
            message = json.loads(text_data)
            print(message)
        elif self.__message_valid__(text_data):
            print("Valid, anonymous")
            message = json.loads(text_data)
            print(message)
        else:
            self.send("Invalid message. Disconnect.")
            self.disconnect(400)

    def __initialize_user__(self, user):
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
