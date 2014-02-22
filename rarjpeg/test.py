from unittest import TestCase
from django.test import SimpleTestCase, LiveServerTestCase
from django.test.utils import override_settings
from admin_honeypot.models import LoginAttempt
import mimetypes
import requests
from urllib.robotparser import RobotFileParser

class SanityTest(TestCase):
    def assertMimeEncoding(self, path, mime, encoding):
        self.assertEqual(mimetypes.guess_type(path), (mime, encoding))

    def test_mime_gzip(self):
        self.assertMimeEncoding('a.css.gz', 'text/css', 'gzip')
        self.assertMimeEncoding('b.js.gz', 'application/javascript', 'gzip')

@override_settings(DEBUG=True)
class BasicTest(SimpleTestCase):
    def test_res_codes(self):
        for url in ('', 'admin/'):
            res = self.client.get('/' + url)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res['Content-Type'][:9], 'text/html')

        res = self.client.get('/favicon.ico')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'][:6], 'image/')

        res = self.client.get('/robots.txt')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res['Content-Type'], 'text/plain')

        res = self.client.get('/not/found')
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res['Content-Type'], 'text/html')

@override_settings(DEBUG=True)
class StaticTest(LiveServerTestCase):
    robots = ('Googlebot', 'Yandex')

    def test_robots_txt(self):
        parser = RobotFileParser(self.live_server_url + '/robots.txt')
        parser.read()

        url = self.live_server_url + '/index.html'
        for robot in self.robots:
            self.assertTrue(parser.can_fetch(robot, url))

        url = self.live_server_url + '/admin/'
        for robot in self.robots:
            self.assertFalse(parser.can_fetch(robot, url))

    def test_res_codes_gzip(self):
        res = requests.get(self.live_server_url + '/pub/pt_sans.css.gz')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/css')
        self.assertEqual(res.headers['Content-Encoding'], 'gzip')

        res = requests.get(self.live_server_url + '/pub/rarjpeg.css')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'text/css')
        self.assertNotIn('Content-Encoding', res.headers)

    def test_vendor_js(self):
        res = requests.get(self.live_server_url + '/pub/vendor/jquery.js')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Type'], 'application/javascript')

class HoneypotTest(SimpleTestCase):
    def test_admin_honeypot(self):
        self.assertEqual(LoginAttempt.objects.count(), 0)
        res = self.client.post('/admin/', {'username': 'admin',
                                           'password': 'admin1'})
        self.assertContains(res, 'Please enter the correct username and '
                            'password for a staff account. Note that both '
                            'fields may be case-sensitive.')
        self.assertEqual(LoginAttempt.objects.count(), 1)
        att = LoginAttempt.objects.get(id=1)
        self.assertEqual(att.username, 'admin')
        self.assertEqual(att.password, 'admin1')
        self.assertEqual(att.ip_address, '127.0.0.1')
