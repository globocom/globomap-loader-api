from globomap_auth_manager import exceptions
from jsonschema.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from globomap_loader_api.api import util
from globomap_loader_api.api.v2 import api
from globomap_loader_api.api.v2.auth.exceptions import AuthException


@api.errorhandler(exceptions.Unauthorized)
@api.header('X-REQUEST-ID', 'Request ID')
def handle_auth_manager_unauthorized_exception(error):
    """Return a custom message and 401 status code"""

    response_header = {'X-REQUEST-ID': util.create_request_id()}

    return {'message': error.message}, 401, response_header


@api.errorhandler(exceptions.InvalidToken)
@api.header('X-REQUEST-ID', 'Request ID')
def handle_auth_manager_invalidtoken_exception(error):
    """Return a custom message and 401 status code"""

    response_header = {'X-REQUEST-ID': util.create_request_id()}

    return {'message': error.message}, 401, response_header


@api.errorhandler(exceptions.AuthException)
@api.header('X-REQUEST-ID', 'Request ID')
def handle_auth_manager_auth_exception(error):
    """Return a custom message and 503 status code"""

    response_header = {'X-REQUEST-ID': util.create_request_id()}

    return {'message': error.message}, 503, response_header


@api.errorhandler(AuthException)
@api.header('X-REQUEST-ID', 'Request ID')
def handle_auth_exception(error):
    """Return a custom message and 503 status code"""

    response_header = {'X-REQUEST-ID': util.create_request_id()}

    return {'message': error.message}, 503, response_header


@api.errorhandler(ValidationError)
@api.header('X-REQUEST-ID', 'Request ID')
def handle_validationerror_exception(error):
    """Return a custom message and 400 status code"""

    response_header = {'X-REQUEST-ID': util.create_request_id()}

    message = {
        'reason': error.message,
        'schema': error.schema
    }

    return {'message': message}, 400, response_header


@api.errorhandler(BadRequest)
@api.header('X-REQUEST-ID', 'Request ID')
def handle_badrequest_exception(error):
    """Return a custom message and 400 status code"""

    response_header = {'X-REQUEST-ID': util.create_request_id()}

    return {'message': str(error)}, 400, response_header


@api.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'message': str(error)}, getattr(error, 'code', 500)
