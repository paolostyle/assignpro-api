from copy import deepcopy
from ap_flow import get_request_validator

test_request = {
    'type': 1,
    'workers': ['A', 'B', 'C'],
    'tasks': ['D', 'E', 'F'],
    'costs': [
        [1, 2, 3],
        [4, 5, 6],
        [9, 8, 7]
    ]
}


def test_request_is_valid():
    rv = get_request_validator()
    assert rv.validate(test_request) == True


def test_unknown_type():
    tr = deepcopy(test_request)
    tr['type'] = 5

    rv = get_request_validator()
    assert rv.validate(tr) == False


def test_non_string_workers():
    tr = deepcopy(test_request)
    tr['workers'][0] = 123

    rv = get_request_validator()
    assert rv.validate(tr) == False


def test_null_cost():
    tr = deepcopy(test_request)
    tr['costs'][1][1] = None

    rv = get_request_validator()
    assert rv.validate(tr) == True


def test_simple_type():
    tr = deepcopy(test_request)
    tr['type'] = 4  # set type to simple mode -> costs should be bools
    tr['costs'] = [
        [True, False, None],
        [False, True, True],
        [None, None, True]
    ]

    rv = get_request_validator()
    assert rv.validate(tr) == True


def test_bool_costs_in_non_simple_type():
    tr = deepcopy(test_request)
    tr['costs'] = [
        [True, False, None],
        [False, True, True],
        [None, None, True]
    ]

    rv = get_request_validator()
    assert rv.validate(tr) == False


def test_too_many_rows():
    tr = deepcopy(test_request)
    tr['costs'].append([])

    rv = get_request_validator()
    assert rv.validate(tr) == False


def test_too_many_values_in_a_row():
    tr = deepcopy(test_request)
    tr['costs'][0].append(12)

    rv = get_request_validator()
    assert rv.validate(tr) == False

