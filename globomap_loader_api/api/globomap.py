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
import logging

from globomap_api_client import auth
from globomap_api_client.collection import Collection
from globomap_api_client.edge import Edge

from globomap_loader_api.settings import GLOBOMAP_API_PASSWORD
from globomap_loader_api.settings import GLOBOMAP_API_URL
from globomap_loader_api.settings import GLOBOMAP_API_USERNAME

LOGGER = logging.getLogger(__name__)


class GloboMapClient(object):

    def __init__(self):
        self.generate_auth()

    def generate_auth(self):
        LOGGER.info('New Auth')
        self.auth = auth.Auth(
            api_url=GLOBOMAP_API_URL,
            username=GLOBOMAP_API_USERNAME,
            password=GLOBOMAP_API_PASSWORD
        )
        self.coll = Collection(auth=self.auth)
        self.edge = Edge(auth=self.auth)

    def get_collections(self, user):
        query = [[{'field': 'user', 'operator': '==', 'value': user}]]
        return self.coll.search(query, page=1, per_page=100)

    def get_edges(self, user):
        query = [[{'field': 'user', 'operator': '==', 'value': user}]]
        return self.edge.search(query, page=1, per_page=100)
