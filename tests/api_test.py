"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import json
import unittest

from mock import patch

from globomap_loader_api.app import create_app
from globomap_loader_api.settings import LOADER_UPDATE
from tests.util import open_json


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
        self._mock_token()

    def tearDown(self):
        self.loader_api_facade.reset_mock()

    @classmethod
    def setUpClass(cls):
        cls.loader_api_facade = patch(
            'globomap_loader_api.app.LoaderAPIFacade._get_rabbit_mq_client').start()

    def test_send_updates(self):
        rabbit_mock = self._mock_rabbitmq_client(True)
        updates = [open_json('tests/json/driver/driver_output_create.json')]
        response = self.app.post(
            '/v2/updates/',
            data=json.dumps(updates),
            headers={'Content-Type': 'application/json'}
        )

        response_json = json.loads(response.data)
        self.assertEqual(202, response.status_code)
        self.assertEqual('Updates published successfully',
                         response_json['message'])
        self.assertEqual(1, rabbit_mock.post_message.call_count)

    def test_send_updates_no_updates_found(self):
        rabbit_mock = self._mock_rabbitmq_client(True)
        response = self.app.post(
            '/v2/updates/',
            data=json.dumps([]),
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(400, response.status_code)
        self.assertDictEqual({'': '[] is too short'},
                             json.loads(response.data)['errors'])
        self.assertEqual(0, rabbit_mock.post_message.call_count)

    def test_send_updates_expected_status_400(self):
        response = self.app.post(
            '/v2/updates/',
            data=json.dumps({'key': 'wrong input'}),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(400, response.status_code)

    def test_send_updates_expected_status_500(self):
        rabbit_mock = self._mock_rabbitmq_client(Exception())
        updates = [open_json('tests/json/driver/driver_output_create.json')]
        response = self.app.post(
            '/v2/updates/',
            data=json.dumps(updates),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(500, response.status_code)
        self.assertEqual(1, rabbit_mock.post_message.call_count)
        self.assertEqual(1, rabbit_mock.discard_publish.call_count)

    def _mock_rabbitmq_client(self, data=None):
        rabbitmq_mock = self.loader_api_facade.return_value

        if type(data) is bool:
            rabbitmq_mock.post_message.return_value = data
            rabbitmq_mock.confirm_publish.return_value = data
        else:
            rabbitmq_mock.post_message.side_effect = data
        return rabbitmq_mock

    def _mock_token(self):
        validate_token = patch(
            'globomap_loader_api.api.v2.auth.decorators.validate_token').start()
        validate_token.return_value.get_token_data_details.return_value = {
            'roles': [{'name': LOADER_UPDATE}]}
