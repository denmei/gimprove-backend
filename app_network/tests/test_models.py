
from django.test import TestCase

from app_network.models.models import Connection, Activity
from app_main.models.models import GymProfile, UserProfile
from django.contrib.auth.models import User


class UserProfileConnectionTest(TestCase):
    """
    Tests interaction between Connections and Userprofiles.
    """

    fixtures = ['fix.json']

    def setUp(self):
        """
        Create two users, one GymProfile and two UserProfiles for following tests.
        :return:
        """
        self.gym = GymProfile.objects.all()[0]
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_2 = User.objects.create_user(username='testuser2', password='12345')
        self.up_1 = UserProfile.objects.create(user=self.user, date_of_birth="1991-11-20", rfid_tag="0123456777")
        self.up_2 = UserProfile.objects.create(user=self.user_2, date_of_birth="1991-11-20", rfid_tag="0123456788")

    def test_connections(self):
        """
        Test whether follower/followed connections are created correctly.
        """
        # create follower connection
        connection = Connection.objects.create(follower=self.user, followed=self.user_2)
        self.assertTrue(self.up_2.get_follower_connections()[0] == connection)
        self.assertTrue(self.up_1.get_follows_connections()[0] == connection)
        self.assertTrue(self.up_1.get_follow_ids()[0] == self.user_2.id)


class UserProfileActivitiesTest(TestCase):
    """
    Tests interaction between Activities and UserProfiles.
    """

    fixtures = ['fix.json']

    def setUp(self):
        """
        Create two users, one GymProfile and two UserProfiles for following tests.
        :return:
        """
        self.gym = GymProfile.objects.all()[0]
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user_2 = User.objects.create_user(username='testuser2', password='12345')
        self.up_1 = UserProfile.objects.create(user=self.user, date_of_birth="1991-11-20", rfid_tag="0123456777")
        self.up_2 = UserProfile.objects.create(user=self.user_2, date_of_birth="1991-11-20", rfid_tag="0123456788")
        self.activity_1 = Activity.objects.create(user=self.user, created="2018-01-03", description="Did a good workout.")

    def test_activities(self):
        """
        Test whether acitvities are created correctly.
        """
        self.assertTrue(self.up_1.get_activities()[0] == self.activity_1)
        self.assertTrue(self.up_2.get_follows_activities()[0] == self.activity_1)