from django.test import SimpleTestCase, LiveServerTestCase
from django.test.utils import override_settings
from urllib.robotparser import RobotFileParser

@override_settings(DEBUG=True)
class BasicTest(SimpleTestCase):
    def test_res_codes(self):
        res = self.client.get('/')
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
class RobotsTest(LiveServerTestCase):
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
