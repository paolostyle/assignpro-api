from ap_flow import FlowNetwork

data = {
    'type': 1,
    'workers': ['A', 'B', 'C'],
    'tasks': ['D', 'E', 'F'],
    'costs': [
        [1, 2, 3],
        [4, 5, 6],
        [9, 8, 7]
    ]
}

expected_array = [
    [8, 7, 6],
    [5, 4, 3],
    [0, 1, 2]
]


def test_costs_for_maximization():
    fn = FlowNetwork(data['workers'], data['tasks'], data['costs'])
    fn.prepare_costs_for_max()
    assert fn.costs == expected_array
