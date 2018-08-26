import time

from django.test import TestCase

from app_tracker.models.models import UserTrackingProfile, Set
from django.utils import timezone

"""
Script to test the models of the tracker app.
"""


class UserProfileTest(TestCase):
    """
    Not necessary since only testing Django-Stuff.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.up = UserTrackingProfile.objects.all()[0]

    def test_auto_deactivation(self):
        """
        Active sets must be deactivated automatically after 15 seconds of inactivity.
        """
        self.up.active_set = Set.objects.first()
        time.sleep(16)
        self.assertEqual(self.up.active_set, None)


class UserProfileActiveSetTest(TestCase):
    """
    Tests whether auto-deactivation of inactive sets works properly.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.up = UserTrackingProfile.objects.first()
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