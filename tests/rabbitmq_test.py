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

from mock import MagicMock
from mock import patch

from globomap_loader_api.rabbitmq import RabbitMQClient


class TestRabbitMQClient(unittest.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_post_message(self):
        pika_mock, channel_mock = self._mock_pika(None)
        rabbitmq = RabbitMQClient('localhost', 5672, 'user', 'password', '/')
        rabbitmq.post_message('exchange', 'key', 'message')

        channel_mock.basic_publish.assert_called_once_with(
            body='message', exchange='exchange',
            routing_key='key',
            properties=pika_mock.BasicProperties(),
            mandatory=True
        )
        pika_mock.BasicProperties.assert_any_call(delivery_mode=2)

    def _mock_pika(self, message):
        pika_mock = patch('globomap_loader_api.rabbitmq.pika').start()
        pika_mock.ConnectionParameters.return_value = MagicMock()
        connection_mock = MagicMock()
        channel_mock = MagicMock()
        connection_mock.channel.return_value = channel_mock
        pika_mock.BlockingConnection.return_value = connection_mock
        channel_mock.basic_get.return_value = (MagicMock(), None, message)
        return pika_mock, channel_mock
