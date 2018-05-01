from channels.generic.websocket import WebsocketConsumer
import json


class SetConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("Connected")

    def disconnect(self, code):
        print("Disconnected")

    def receive(self, text_data=None, bytes_data=None):
        pass
