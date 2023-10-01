from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Token


class TestAPI(APITestCase):

    url = ''

    def setUp(self) -> None:
        Token.objects.create(
            full_url='https://ya.by/',
            short_url='Sop2ER',
        )

    def test_token_get(self):
        existing_data = {
            'full_url': 'https://ya.by/'
        }
        response_get = self.client.post(self.url, data=existing_data, content_type='application/json',
                                        HTTP_ACCEPT='application/json')
        result_get = response_get.json()

        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get['Content-Type'], 'application/json')
        self.assertEqual(Token.objects.all().count(), 1)
        self.assertEqual(result_get['full_url'], 'https://ya.by/')
        self.assertEqual(result_get['short_url'], 'Sop2ER')
        self.assertIsInstance(result_get, dict)
        self.assertEqual(len(result_get), 6)

    def test_token_create(self):
        creation_data = {
            'full_url': 'http://post.url.test.by'
        }
        creation_full_data = {
            'full_url': 'http://test.by',
            'short_url': 'TRy293'
        }
        response_create = self.client.post(self.url, data=creation_data)
        result_create = response_create.json()

        response_create_with_short_url = self.client.post(
            self.url, data=creation_full_data
        )
        result_create_with_short_url = response_create_with_short_url.json()

        self.assertEqual(response_create.status_code, 201)
        self.assertEqual(result_create['full_url'], 'http://post.url.test.by')
        self.assertEqual(len(result_create['short_url']), 6)
        self.assertIsInstance(result_create, dict)
        self.assertEqual(Token.objects.all().count(), 3)
        self.assertEqual(len(result_create), 6)
        self.assertEqual(
            result_create_with_short_url['full_url'],
            'http://test.by',
            msg='Ошибка full_url'
        )
        self.assertEqual(
            result_create_with_short_url['short_url'],
            'TRy293',
            msg='Ошибка short_url'
        )


class TestRedirection(TestCase):
    active_url = '/Sop2ER'
    deactive_url = '/TRy293'

    def setUp(self) -> None:
        Token.objects.create(
            full_url='https://ya.by/',
            short_url='Sop2ER',
        )

        Token.objects.create(
            full_url='https://onliner.by/',
            short_url='TRy293',
            is_active=False
        )

    def test_redirection(self):
        response = self.client.get(self.active_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'https://ya.by/')

    def test_response_counter(self):
        self.assertEqual(
            Token.objects.get(short_url='Sop2ER').requests_count, 0
        )
        self.client.get(self.active_url)
        self.assertEqual(
            Token.objects.get(short_url='Sop2ER').requests_count, 1
        )
        self.assertEqual(
            Token.objects.get(short_url='TRy293').requests_count, 0
        )
        self.client.get(self.deactive_url)
        self.assertEqual(
            Token.objects.get(short_url='TRy293').requests_count, 0
        )

    def test_deactive_url(self):
        response = self.client.get(self.deactive_url)
        self.assertEqual(response.content, b'Token is no longer available')
