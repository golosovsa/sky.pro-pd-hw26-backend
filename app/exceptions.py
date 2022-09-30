class BaseServiceError(Exception):
    code = 500


class ItemNotFound(BaseServiceError):
    code = 404


class BadRequestParameters(BaseServiceError):
    code = 400


class BadRequestData(BaseServiceError):
    code = 400
