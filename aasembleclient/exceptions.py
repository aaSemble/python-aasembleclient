class AasembleClientException(Exception):
    pass

class InvalidDataException(AasembleClientException):
    def __init__(self, error_detail):
        self.error_detail = error_detail

    def __str__(self):
        return '\n'.join(['%s: %s' % (k, v) for (k, v) in self.error_detail.items()])
