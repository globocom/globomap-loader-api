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
from jsonspec.validators.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

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
@api.header(
    'x-driver-name',
    'Name of Driver',
    required=True,
    default=''
)
class Updates(Resource):

    @api.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden'
    })
    @permission_classes((permissions.Update,))
    @api.expect(api.schema_model('PostUpdates',
                                 util.get_dict(SPECS.get('updates'))))
    def post(self):
        """Post a list of messages."""

        try:
            data = request.get_json()
            driver_name = request.headers.get('X-DRIVER-NAME', '*')
            app.config['LOADER_RMQ'].publish_updates(
                data, driver_name)
            res = {
                'message': 'Updates published successfully',
            }

            return res, 202

        except ValidationError as error:
            app.logger.exception('Error sending updates to rabbitmq')
            api.abort(400, errors=util.validate(error))
        except BadRequest as err:
            app.logger.exception('Error sending updates to rabbitmq')
            api.abort(400, errors=err.description)
        except:
            app.logger.exception('Error sending updates to rabbitmq')
            res = {'message': 'Error sending updates to queue'}
            return api.abort(500, errors=res)
