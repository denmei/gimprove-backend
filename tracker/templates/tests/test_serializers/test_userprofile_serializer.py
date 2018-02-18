from rest_framework.test import APITestCase, RequestsClient
from tracker.serializers.UserProfileSerializer import *


class UserProfileSerializerTest(APITestCase):
    """
    Tests the functionality of the UserSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"
        self.rfid_tag = UserProfile.objects.all()[0].rfid_tag
        self.user = UserProfile.objects.all()[0].user
        self.active_set = UserProfile.objects.all()[0].active_set

    def test_userprofile_retrieval(self):
        """
        Tests whether a UserProfile can be retrieved properly by the User-Id.
        """
        response = self.c.get(self.pre_http + reverse('userprofile_detail', kwargs={'pk': self.user.id}))
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)
        if content['active_set'] is None:
            self.assertEqual(content['active_set'], self.active_set)
        else:
            self.assertEqual(content['active_set'], str(self.active_set))

    def test_userprofile_retrieval_rfid(self):
        """
        Tests whether a UserProfile can be retrieved properly by the User-RFID-Number.
        """
        response = self.c.get(self.pre_http + reverse('userprofile_rfid_detail', kwargs={'rfid_tag': self.rfid_tag}))
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)
        if content['active_set'] is None:
            self.assertEqual(content['active_set'], self.active_set)
        else:
            self.assertEqual(content['active_set'], str(self.active_set))
        self.assertEqual(content['user'], self.user.id)
