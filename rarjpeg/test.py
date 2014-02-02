from django.test import SimpleTestCase
from django.test.utils import override_settings

class BasicTest(SimpleTestCase):
    @override_settings(DEBUG=True)
    def test_res_codes(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/html')

        res = self.client.get('/favicon.ico')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'][:6], 'image/')

        res = self.client.get('/robots.txt')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/plain')

        res = self.client.get('/not/found')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res['Content-Type'], 'text/html')
