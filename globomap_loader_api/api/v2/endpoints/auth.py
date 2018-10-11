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
from flask import current_app as app
from flask import request
from flask_restplus import Resource
from globomap_auth_manager import exceptions

from globomap_loader_api.api.util import get_dict
from globomap_loader_api.api.v2 import api
from globomap_loader_api.api.v2.auth import facade
from globomap_loader_api.api.v2.auth.exceptions import AuthException
from globomap_loader_api.settings import SPECS

ns = api.namespace(
    'auth', description='Operations related to auth')


@ns.route('/')
class CreateAuth(Resource):

    @api.doc(responses={
        200: 'Success',
        401: 'Unauthorized',
        503: 'Service Unavailable'
    })
    @api.expect(api.schema_model('Auth', get_dict(SPECS.get('auth'))))
    def post(self):
        """Create token"""

        try:
            data = request.get_json()
            if type(data) is dict:
                username = data.get('username')
                password = data.get('password')
            else:
                username = None
                password = None
            if not username or not password:
                app.logger.error('Username and Password is required.')
                api.abort(401, errors='Username and Password is required.')

            token = facade.create_token(username, password)
            return token, 200

        except exceptions.Unauthorized:
            app.logger.error('User %s not Unauthorized.', username)
            api.abort(401, 'User not Unauthorized.')

        except exceptions.AuthException:
            app.logger.error('Auth Unavailable.')
            api.abort(503, 'Auth Unavailable.')

        except AuthException:
            app.logger.error('Auth Unavailable.')
            api.abort(503, 'Auth Unavailable.')
