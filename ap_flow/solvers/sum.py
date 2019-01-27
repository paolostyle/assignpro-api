from math import inf
from ortools.graph import pywrapgraph
from .. import FlowNetwork, Calculation, CalcType, make_response


def solve(fn: FlowNetwork, maximize: bool=False, threshold=inf):
    graph = pywrapgraph.SimpleMinCostFlow()

    calc_type = CalcType.SUM

    if maximize:
        fn.prepare_costs_for_max()
        calc_type = CalcType.SUM_MAX

    if threshold is not inf:
        calc_type = CalcType.BOTTLENECK

    for worker in fn.workers_nodes:
        graph.AddArcWithCapacityAndUnitCost(
            fn.source, worker, 1, 0
        )

    for i in range(len(fn.workers)):
        for j in range(len(fn.tasks)):
            if fn.costs[i][j] is not None and fn.costs[i][j] <= threshold:
                graph.AddArcWithCapacityAndUnitCost(
                    fn.workers_nodes[i], fn.tasks_nodes[j], 1, fn.costs[i][j]
                )

    for task in fn.tasks_nodes:
        graph.AddArcWithCapacityAndUnitCost(task, fn.sink, 1, 0)

    # supply has to be the lower of the two to make sure that
    # all of them are assigned when the costs matrix isn't square
    supply = min(len(fn.tasks), len(fn.workers))

    graph.SetNodeSupply(fn.source, supply)
    graph.SetNodeSupply(fn.sink, -supply)

    solution = graph.Solve()

    if solution == graph.OPTIMAL:
        assignment = Calculation(calc_type, fn, graph).parse_solution()
        return make_response(assignment, 200)
    else:
        return make_response({}, 400)
