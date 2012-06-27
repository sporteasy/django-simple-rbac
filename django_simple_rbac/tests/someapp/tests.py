from django.test import TestCase
from django.test.client import Client, RequestFactory


class AclTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def _test_permission_denied(self, response):
        self.assertEqual(response.status_code, 403)

    def _test_permission_granted(self, response):
        self.assertEqual(response.status_code, 200)

    def test_as_anonymous(self):
        client = Client()

        # test list
        response = client.get('/post/list')
        self._test_permission_granted(response)

        # test view
        response = client.get('/post/view')
        self._test_permission_granted(response)

        # test update
        response = client.get('/post/update')
        self._test_permission_denied(response)
        

