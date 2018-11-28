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

from globomap_loader_api.rabbitmq import RabbitMQClient
from globomap_loader_api.settings import GLOBOMAP_RMQ_EXCHANGE
from globomap_loader_api.settings import GLOBOMAP_RMQ_HOST
from globomap_loader_api.settings import GLOBOMAP_RMQ_KEY
from globomap_loader_api.settings import GLOBOMAP_RMQ_PASSWORD
from globomap_loader_api.settings import GLOBOMAP_RMQ_PORT
from globomap_loader_api.settings import GLOBOMAP_RMQ_USER
from globomap_loader_api.settings import GLOBOMAP_RMQ_VIRTUAL_HOST


LOGGER = logging.getLogger(__name__)


class LoaderAPIFacade(object):

    def __init__(self):
        self.rabbitmq = self._get_rabbit_mq_client()

    def _get_rabbit_mq_client(self):
        return RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def publish_updates(self, updates, headers):
        if updates:
            try:
                for update in updates:
                    self.rabbitmq.post_message(
                        exchange=GLOBOMAP_RMQ_EXCHANGE,
                        key=GLOBOMAP_RMQ_KEY,
                        message=json.dumps(update, ensure_ascii=False),
                        headers=headers
                    )
                return None
            except Exception:
                LOGGER.exception('Failed to send updates to queue')
                raise Exception('Failed to send updates to queue')

    def publish_spec(self, queue, spec):
        try:
            self.rabbitmq.post_message(
                queue=queue,
                message=json.dumps(spec, ensure_ascii=False),
            )
        except Exception:
            LOGGER.exception('Failed to send spec to queue')
            raise Exception('Failed to send spec to queue')
