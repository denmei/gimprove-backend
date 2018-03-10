import time

from django.test import TestCase

from tracker.models.models import *

"""
Script to test the models of the tracker app.
"""


class UserProfileTest(TestCase):
    """
    Not necessary since only testing Django-Stuff.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.up = UserProfile.objects.all()[0]
        self.gym = GymProfile.objects.all()[0]

    def create_userprofile(self, gym, rfid_tag, date_of_birth="1991-11-20",):
        return UserProfile.objects.create(date_of_birth=date_of_birth, rfid_tag=rfid_tag)

    def test_userprofile_creation(self):
        self.up = self.create_userprofile(self.gym, "0123456789")
        self.assertTrue(isinstance(self.up, UserProfile))

    def test_auto_deactivation(self):
        self.up.active_set = Set.objects.first()
        time.sleep(16)
        self.assertEqual(self.up.active_set, None)


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


class UserProfileActiveSetTest(TestCase):
    """
    Tests whether auto-deactivation of inactive sets works properly.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.up = UserProfile.objects.first()
        self.set = Set.objects.first()
        self.set.last_update = timezone.now()
        self.up.active_set = self.set

    def test_no_deactivation_after_update(self):
        time.sleep(5)
        self.set.last_update = timezone.now()
        time.sleep(11)
        self.assertTrue(self.up.active_set == self.set)

    def test_deactivation_no_update(self):
        self.up.active_set = self.set
        self.set.last_update = timezone.now() - timezone.timedelta(seconds=16)
        self.assertTrue(self.up.active_set is None)


#TODO: Test function "get_profile_type"