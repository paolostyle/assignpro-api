import numpy as np
from ortools.graph import pywrapgraph
from .. import FlowNetwork
from . import sum


def get_unique_costs(costs):
    np_costs = np.array(costs, dtype=np.float).flatten()
    np_costs = np_costs[~np.isnan(np_costs)]
    np_costs = np.unique(np_costs).astype(int)
    return list(np_costs)


def check_threshold(fn: FlowNetwork, threshold):
    graph = pywrapgraph.SimpleMaxFlow()

    for worker in fn.workers_nodes:
        graph.AddArcWithCapacity(fn.source, worker, 1)

    for i in range(len(fn.workers)):
        for j in range(len(fn.tasks)):
            if fn.costs[i][j] is not None and fn.costs[i][j] <= threshold:
                graph.AddArcWithCapacity(
                    fn.workers_nodes[i], fn.tasks_nodes[j], 1
                )

    for task in fn.tasks_nodes:
        graph.AddArcWithCapacity(task, fn.sink, 1)

    solution = graph.Solve(fn.source, fn.sink)

    req_flow = min(len(fn.workers), len(fn.tasks))

    return solution == graph.OPTIMAL and req_flow == graph.OptimalFlow()


def solve(fn: FlowNetwork):
    thresholds = get_unique_costs(fn.costs)
    min_index = 0
    max_index = len(thresholds) - 1
    threshold_index = max_index

    while max_index >= min_index:
        mid = (min_index + max_index) // 2
        if check_threshold(fn, thresholds[mid]):
            threshold_index = mid
            max_index = mid - 1
        else:
            min_index = mid + 1

    threshold = int(thresholds[threshold_index])

    response = sum.solve(fn, False, threshold)
    response['numResult'] = threshold

    return response
