from django.test import SimpleTestCase

class BasicTest(SimpleTestCase):
    def test_res_codes(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)

        res = self.client.get('/not/found')
        self.assertEqual(res.status_code, 404)
