from ap_flow.solvers import sum, bottleneck, simple
from ap_flow import FlowNetwork, CalcType

data = {
    'tasks': ['A', 'B', 'C', 'D'],
    'workers': ['1', '2', '3', '4'],
    'costs': [
        [80, 40, 50, 46],
        [40, 70, 20, 25],
        [30, 10, 20, 30],
        [35, 20, 25, 30]
    ]
}


def test_sum_solver():
    expected_assignment = [{
        'worker': '1',
        'task': 'D',
        'value': 46,
        'row': 1,
        'col': 4
    }, {
        'worker': '2',
        'task': 'C',
        'value': 20,
        'row': 2,
        'col': 3
    }, {
        'worker': '3',
        'task': 'B',
        'value': 10,
        'row': 3,
        'col': 2
    }, {
        'worker': '4',
        'task': 'A',
        'value': 35,
        'row': 4,
        'col': 1
    }]

    expected_result = {
        'type': CalcType.SUM,
        'assignment': expected_assignment,
        'numResult': 111,
        'message': 'Obliczenia zakończone sukcesem!',
        'status': 200,
        'calculationDate': 0    # rather irrelevant
    }

    test_fn = FlowNetwork(data['workers'], data['tasks'], data['costs'])

    response = sum.solve(test_fn)
    response['calculationDate'] = 0

    assert response == expected_result


def test_bottleneck_solver():
    """
    Overall assignment is not really relevant in this case,
    so we're only checking if the num_result (so the "bottleneck")
    is equal 40 which is the correct result for this data
    and if assignment object with that value exists in overall assignment.
    """
    expected_num_result = 40
    bottleneck_assignment = {
        'worker': '1',
        'task': 'B',
        'value': 40,
        'row': 1,
        'col': 2
    }

    test_fn = FlowNetwork(data['workers'], data['tasks'], data['costs'])
    response = bottleneck.solve(test_fn)

    assert (response['numResult'] == expected_num_result
            and bottleneck_assignment in response['assignment'])


def test_simple_solver():
    data = {
        'tasks': ['A', 'B', 'C'],
        'workers': ['1', '2', '3'],
        'costs': [
            [True, False, True],
            [False, True, False],
            [True, True, False],
        ]
    }

    expected_result = {
        'type': CalcType.SIMPLE,
        'assignment': [{
            'worker': '1',
            'task': 'C',
            'value': 0,
            'row': 1,
            'col': 3
        }, {
            'worker': '2',
            'task': 'B',
            'value': 0,
            'row': 2,
            'col': 2
        }, {
            'worker': '3',
            'task': 'A',
            'value': 0,
            'row': 3,
            'col': 1
        }],
        'numResult': 3,
        'message': 'Obliczenia zakończone sukcesem!',
        'status': 200,
        'calculationDate': 0    # rather irrelevant
    }

    test_fn = FlowNetwork(data['workers'], data['tasks'], data['costs'])
    response = simple.solve(test_fn)
    response['calculationDate'] = 0

    assert response == expected_result
