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
import pika


class RabbitMQClient(object):

    def __init__(self, host, port, user, password, vhost):
        credentials = pika.PlainCredentials(user, password)
        parameters = pika.ConnectionParameters(
            host=host, port=port,
            virtual_host=vhost, credentials=credentials
        )
        self.parameters = parameters
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def verify_connection(self):
        if self.connection.is_closed or self.connection.is_closing:
            self.connect()

    def post_message(self, exchange_name, key, message, headers, confirm=True):
        self.verify_connection()
        try:
            published = self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=key,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers=headers
                ),
                mandatory=True
            )
        except pika.exceptions.ConnectionClosed:
            self.connect()
            return self.post_message(exchange_name, key, message, headers, confirm)

        if published and confirm:
            self.confirm_publish()
        return confirm

    def confirm_publish(self):
        self.channel.tx_select()
        self.channel.tx_commit()

    def discard_publish(self):
        self.channel.tx_select()
        self.channel.tx_rollback()
