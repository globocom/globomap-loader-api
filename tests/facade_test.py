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
import unittest

from mock import call
from mock import patch

from globomap_loader_api.api.facade import LoaderAPIFacade


class TestLoaderAPIFacade(unittest.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_publish_updates_exception(self):
        rmq_mock = self.mock_rmqclient()
        rmq_mock.post_message.side_effect = Exception()

        with self.assertRaises(Exception):
            loader_facade = LoaderAPIFacade()
            updates = [{'key': 'value'}, {'key2': 'value2'}]
            headers = {'header_1': 'value_1'}
            loader_facade.publish_updates(updates=updates, headers=headers)

    def test_publish_updates(self):
        rmq_mock = self.mock_rmqclient()
        rmq_mock.post_message.return_value = True

        loader_facade = LoaderAPIFacade()

        updates = [{'key': 'value'}, {'key2': 'value2'}]
        headers = {'header_1': 'value_1'}
        loader_facade.publish_updates(updates=updates, headers=headers)

        loader_facade.rabbitmq.post_message.assert_has_calls([
            call(exchange='globomap-updates-exchange',
                 key='globomap.updates',
                 message='{"key": "value"}',
                 headers={'header_1': 'value_1'}
                 ),
            call(exchange='globomap-updates-exchange',
                 key='globomap.updates',
                 message='{"key2": "value2"}',
                 headers={'header_1': 'value_1'}
                 )
        ])

        self.assertEqual(2, loader_facade.rabbitmq.post_message.call_count)

    def test_publish_spec(self):
        rmq_mock = self.mock_rmqclient()
        rmq_mock.post_message.return_value = True

        loader_facade = LoaderAPIFacade()

        spec = {'key': 'value'}
        loader_facade.publish_spec('queue_1', spec)

        loader_facade.rabbitmq.post_message.assert_has_calls([
            call(
                queue='queue_1',
                message='{"key": "value"}'
            )
        ])

        self.assertEqual(1, loader_facade.rabbitmq.post_message.call_count)

    def mock_rmqclient(self):
        rmq_mock = patch(
            'globomap_loader_api.api.facade.RabbitMQClient').start()

        return rmq_mock.return_value
