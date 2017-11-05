

class SesError(Exception):
    pass


class ImproperlyConfigured(SesError):
    pass


class SchemaValidationError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

    def __str__(self):
        err = super().__str__()
        return "%s: %s" % (err, self.errors)
