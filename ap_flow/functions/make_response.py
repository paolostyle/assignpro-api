from datetime import datetime


def make_response(response, status, v_errors=None):
    response['status'] = status

    if status == 200:
        msg = 'success'
    elif status == 400 and v_errors == None:
        msg = 'assignment_impossible'
    elif status == 400 and v_errors != None:
        msg = 'validation_error'
    elif status == 416:
        msg = 'costs_overflow'
    elif status == 500:
        msg = 'internal_server_error'
    elif status == 501:
        msg = 'invalid_calculation_type'

    response['message'] = msg
    response['calculationDate'] = datetime.now().isoformat()
    return response
