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
from logging import config

from flask import Flask

from globomap_loader_api.api.facade import LoaderAPIFacade
from globomap_loader_api.api.v1.api import blueprint as api_v1
from globomap_loader_api.api.v2.api import blueprint as api_v2
from globomap_loader_api.settings import LOGGING


def create_app():

    app = Flask(__name__)
    app.config['LOGGER_HANDLER_POLICY'] = 'default'
    app.config['LOGGER_NAME'] = 'globomap_loader_api'
    app.config['BUNDLE_ERRORS'] = True
    app.config['ERROR_404_HELP'] = False
    app.config.from_object('globomap_loader_api.settings')

    app.logger
    config.dictConfig(LOGGING)

    app.config['LOADER_RMQ'] = LoaderAPIFacade()

    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)

    return app
