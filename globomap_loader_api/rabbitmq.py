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
import logging

import pika

LOGGER = logging.getLogger(__name__)


class RabbitMQClient(object):

    def __init__(self, host, port, user, password, vhost):
        self._params = pika.ConnectionParameters(
            host=host, port=port, virtual_host=vhost,
            credentials=pika.PlainCredentials(user, password))
        self._conn = None
        self._channel = None
        self.connect()

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(self._params)
            self._channel = self._conn.channel()

    def _publish_exchange(self, **kwargs):
        self._channel.confirm_delivery()
        published = self._channel.basic_publish(
            exchange=kwargs.get('exchange'),
            routing_key=kwargs.get('key'),
            body=kwargs.get('message'),
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers=kwargs.get('headers')
            ),
            mandatory=True
        )
        return published

    def _publish_queue(self, **kwargs):
        self._channel.confirm_delivery()
        published = self._channel.basic_publish(
            exchange='',
            routing_key=kwargs.get('queue'),
            body=kwargs.get('message'),
            properties=pika.BasicProperties(
                delivery_mode=2,
                headers=kwargs.get('headers')
            ),
            mandatory=True
        )
        return published

    def post_message(self, **kwargs):
        """Publish message, reconnecting if necessary."""
        if kwargs.get('exchange'):
            publish = self._publish_exchange
        else:
            publish = self._publish_queue

        try:
            return publish(**kwargs)
        except pika.exceptions.ConnectionClosed:
            self.connect()
            return publish(**kwargs)

    def setup_queue(self, queue_name):
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.
        :param str|unicode queue_name: The name of the queue to declare.
        """
        LOGGER.info('Declaring queue %s', queue_name)
        self._channel.queue_declare(
            queue=queue_name,
            arguments={'x-message-ttl': 1800000}
        )

    def get_message(self, queue):
        method_frame, _, body = self._channel.basic_get(queue)
        if body:
            body = json.loads(body)
            return body, method_frame.delivery_tag
        else:
            return None, None

    def nack_message(self, delivery_tag):
        self._channel.basic_nack(delivery_tag)
