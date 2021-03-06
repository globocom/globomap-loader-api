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

from globomap_loader_api.api import util
from globomap_loader_api.api.v2 import api
from globomap_loader_api.api.v2.auth import permissions
from globomap_loader_api.api.v2.auth.decorators import permission_classes
from globomap_loader_api.settings import SPECS


ns = api.namespace(
    'updates', description='Operations related to updates')


@ns.route('/')
@api.header(
    'Authorization',
    'Token Authorization',
    required=True,
    default='Token token='
)
class Updates(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        503: 'Service Unavailable'
    })
    @permission_classes((permissions.Update,))
    @api.expect(api.schema_model('PostUpdates',
                                 util.get_dict(SPECS.get('updates'))))
    def post(self, **kwargs):
        """Post a list of messages."""
        response_header = {'X-REQUEST-ID': util.create_request_id()}
        auth_inst = kwargs['auth_inst']
        data = request.get_json()
        app.config['LOADER_RMQ'].publish_updates(
            updates=data, headers=response_header, auth_inst=auth_inst)
        res = {
            'message': 'Updates published successfully',
        }

        return res, 202, response_header
