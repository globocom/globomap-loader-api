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
from globomap_loader_api.api.v2 import api
from globomap_loader_api.api.v2 import blueprint
from globomap_loader_api.api.v2.endpoints.auth import ns as auth_ns
from globomap_loader_api.api.v2.endpoints.driver_api import ns as driver_api_namespace
from globomap_loader_api.api.v2.endpoints.healthcheck import ns as healthcheck_ns

api.add_namespace(auth_ns)
api.add_namespace(driver_api_namespace)
api.add_namespace(healthcheck_ns)

__all__ = ['api', 'blueprint']
