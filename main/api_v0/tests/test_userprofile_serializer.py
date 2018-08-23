from django.test.utils import override_settings
from rest_framework.test import APITestCase, RequestsClient
from main.models.models import UserProfile, GymProfile, User
import json
from django.urls import reverse


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
        self.gym = GymProfile.objects.first()
        self.header = {'Authorization': 'Token ' + str(self.user.auth_token)}

    @override_settings(DEBUG=True)
    def test_userprofile_creation(self):
        """
        Tests whether UserProfiles can be created properly using the API.
        """
        data = {'date_of_birth': "1991-11-20", 'gym': self.gym.user.id, 'rfid_tag': "1234567890",
                'achievements': None, 'active_set': None, 'bio': "Test", 'profile_image': None,
                'username': 'test create'}
        response = self.c.post(self.pre_http + reverse('userprofile_create'), data, headers=self.header)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserProfile.objects.last().gym.first(), self.gym)

    def test_userprofile_delete(self):
        """
        Tests whether a UserProfile and -account can be deleted and reactivated properly.
        """
        # create account
        data = {'date_of_birth': "1991-11-20", 'gym': self.gym.user.id, 'rfid_tag': "1234567890",
                'achievements': None, 'active_set': None, 'bio': "Test", 'profile_image': None,
                'username': 'test delete'}
        response_id = json.loads(self.c.post(self.pre_http + reverse('userprofile_create'), data, headers=self.header)
                                 .content.decode("utf-8"))['user']
        active_users_1 = len(User.objects.filter(is_active=True))
        users_1 = len(User.objects.all())
        # delete account
        delete_request = self.c.delete(self.pre_http + reverse('userprofile_detail'), headers=self.header)
        active_users_2 = len(User.objects.filter(is_active=True))
        users_2 = len(User.objects.all())
        self.assertEqual(delete_request.status_code, 204)
        self.assertEqual(active_users_1, active_users_2 + 1)
        self.assertEqual(users_1, users_2)

    def test_userprofile_retrieval(self):
        """
        Tests whether a UserProfile can be retrieved properly by the User-Id.
        """
        response = self.c.get(self.pre_http + reverse('userprofile_detail'), headers=self.header)
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)
        if content['_pr_active_set'] is None:
            self.assertEqual(content['_pr_active_set'], self.active_set)
        else:
            self.assertEqual(content['_pr_active_set'], str(self.active_set))

    def test_userprofile_retrieval_rfid(self):
        """
        Tests whether a UserProfile can be retrieved properly by the User-RFID-Number.
        """
        response = self.c.get(self.pre_http + reverse('userprofile_rfid_detail', kwargs={'rfid_tag': self.rfid_tag}),
                              headers=self.header)
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)
        if content['_pr_active_set'] is None:
            self.assertEqual(content['_pr_active_set'], self.active_set)
        else:
            self.assertEqual(content['_pr_active_set'], str(self.active_set))
        self.assertEqual(content['user'], self.user.id)

    # TODO: Add test for unauthorized userprofile-request
