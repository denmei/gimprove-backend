from django.urls import reverse, resolve
from django.test import TestCase


class UrlTest(TestCase):

    def setUp(self):
        pass

    def test_userprofile_detal_urls(self):
        url_detail = reverse('userprofile_detail')
        resolved_detail = resolve(url_detail)
        self.assertEqual(url_detail, '/api_v0_main/userprofile_detail_rest/')
        self.assertEqual(resolved_detail.view_name, "userprofile_detail")

        url_rfid = reverse('userprofile_rfid_detail', args=[1])
        resolved_rfid = resolve(url_rfid)
        self.assertEqual(url_rfid, '/api_v0_main/userprofile_detail_rfid_rest/1')
        self.assertEqual(resolved_rfid.view_name, "userprofile_rfid_detail")

        url_create = reverse('userprofile_create')
        resolved_create = resolve(url_create)
        self.assertEqual(url_create, '/api_v0_main/userprofile_create_rest/')
        self.assertEqual(resolved_create.view_name, "userprofile_create")
