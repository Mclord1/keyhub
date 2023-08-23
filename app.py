import os
import traceback
from botocore.exceptions import ClientError
from application import app
from application.utils.output import OutputObj
from application.utils.output import return_json
from exceptions.custom_exception import CustomException

EXEC_ENV = os.environ.get('EXEC_ENV')


@app.errorhandler(Exception)
def error_handling(error):
    traceback.print_exc()
    message = 'Internal server error!!!!!'
    code = 500
    response_code = 1000
    if isinstance(error, ClientError):
        message = error.response.get('Error', {}).get(
            'Code') + " : " + error.response.get('Error', {}).get('Message')
        code = 400
    elif isinstance(error, CustomException):
        message = error.message
        response_code = error.response_code
        code = error.status_code
    else:
        error = CustomException()
        message = error.message
        code = error.status_code
    output = OutputObj(code=code, message=message, response_code=response_code)
    return return_json(output)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
