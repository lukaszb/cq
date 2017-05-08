

class SesError(Exception):
    pass


class ImproperlyConfigured(SesError):
    pass


class SchemaValidationError(Exception):
    pass
