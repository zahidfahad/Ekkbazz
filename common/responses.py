from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.utils.translation import gettext_lazy as _

STATUS_CODES = {
    100: status.HTTP_100_CONTINUE,
    101: status.HTTP_101_SWITCHING_PROTOCOLS,
    200: status.HTTP_200_OK,
    201: status.HTTP_201_CREATED,
    202: status.HTTP_202_ACCEPTED,
    203: status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    204: status.HTTP_204_NO_CONTENT,
    205: status.HTTP_205_RESET_CONTENT,
    206: status.HTTP_206_PARTIAL_CONTENT,
    207: status.HTTP_207_MULTI_STATUS,
    208: status.HTTP_208_ALREADY_REPORTED,
    226: status.HTTP_226_IM_USED,
    300: status.HTTP_300_MULTIPLE_CHOICES,
    301: status.HTTP_301_MOVED_PERMANENTLY,
    301: status.HTTP_302_FOUND,
    303: status.HTTP_303_SEE_OTHER,
    304: status.HTTP_304_NOT_MODIFIED,
    305: status.HTTP_305_USE_PROXY,
    306: status.HTTP_306_RESERVED,
    307: status.HTTP_307_TEMPORARY_REDIRECT,
    308: status.HTTP_308_PERMANENT_REDIRECT,
    400: status.HTTP_400_BAD_REQUEST,
    401: status.HTTP_401_UNAUTHORIZED,
    402: status.HTTP_402_PAYMENT_REQUIRED,
    403: status.HTTP_403_FORBIDDEN,
    404: status.HTTP_404_NOT_FOUND,
    405: status.HTTP_405_METHOD_NOT_ALLOWED,
    406: status.HTTP_406_NOT_ACCEPTABLE,
    407: status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED,
    408: status.HTTP_408_REQUEST_TIMEOUT,
    409: status.HTTP_409_CONFLICT,
    410: status.HTTP_410_GONE,
    411: status.HTTP_411_LENGTH_REQUIRED,
    412: status.HTTP_412_PRECONDITION_FAILED,
    413: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    414: status.HTTP_414_REQUEST_URI_TOO_LONG,
    415: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    416: status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,
    417: status.HTTP_417_EXPECTATION_FAILED,
    422: status.HTTP_422_UNPROCESSABLE_ENTITY,
    423: status.HTTP_423_LOCKED,
    424: status.HTTP_424_FAILED_DEPENDENCY,
    426: status.HTTP_426_UPGRADE_REQUIRED,
    428: status.HTTP_428_PRECONDITION_REQUIRED,
    429: status.HTTP_429_TOO_MANY_REQUESTS,
    431: status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
    451: status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS,
    500: status.HTTP_500_INTERNAL_SERVER_ERROR,
    501: status.HTTP_501_NOT_IMPLEMENTED,
    502: status.HTTP_502_BAD_GATEWAY,
    503: status.HTTP_503_SERVICE_UNAVAILABLE,
    504: status.HTTP_504_GATEWAY_TIMEOUT,
    505: status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED,
    506: status.HTTP_506_VARIANT_ALSO_NEGOTIATES,
    507: status.HTTP_507_INSUFFICIENT_STORAGE,
    508: status.HTTP_508_LOOP_DETECTED,
    509: status.HTTP_509_BANDWIDTH_LIMIT_EXCEEDED,
    510: status.HTTP_510_NOT_EXTENDED,
    511: status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED,
}

VALIDATION_ERROR = _("Validation Error")

def success_response(status_code, message, data=None, **kwargs):
    response = {"success": True, "message": message}
    if data != None:
        response["data"] = data
    response = {**response, **kwargs}

    if status_code == 204:
        response = None

    return Response(response, status=STATUS_CODES[status_code])


def error_response(status_code, message, **kwargs):
    response = {"success": False, "message": message}
    response = {**response, **kwargs}

    return Response(response, status=STATUS_CODES[status_code])

def raise_error(status_code, message, **kwargs):
    response = {"success": False, "message": message}
    response = {**response, **kwargs}

    raise serializers.ValidationError(response)


def get_plain_error_message_from_exception(error_object):
    if isinstance(error_object, ValidationError):
        error_field = list(error_object.detail.keys())[0]
        return error_object.detail[error_field][0].capitalize()
    elif isinstance(error_object, Exception):
        return error_object.__str__()
    else:
        return error_object
    

class ListPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 200

    def get_paginated_response(self, message, data):
        return Response(
            {
                "success": True,
                "messsage": message,
                "count": self.page.paginator.count,
                "links": {"next": self.get_next_link(), "previous": self.get_previous_link()},
                "data": data,
            }
        )
