from exceptions.codes import ExceptionCode


class CustomException(Exception):
    def __init__(self, exception_code=None, status_code=500, payload=None, response_code=1999,
                 message="Internal Server Error. Please try again later"):
        Exception.__init__(self)

        if isinstance(exception_code, ExceptionCode):
            self.message = exception_code.value['message']
            self.status_code = exception_code.value['status_code']
            self.response_code = exception_code.value['response_code']
        else:
            self.message = message
            self.status_code = status_code
            self.response_code = response_code

        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status_code'] = self.status_code
        rv['response_code'] = self.response_code
        return rv

    def __str__(self):
        return f"{self.status_code} - {self.message}"

    def __repr__(self):
        return f"CustomException({self.status_code}, '{self.message}')"

# Dummy change to trigger deployment
