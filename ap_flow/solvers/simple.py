from ortools.graph import pywrapgraph
from .. import FlowNetwork, CalcType, make_response, Calculation


def solve(fn: FlowNetwork):
    graph = pywrapgraph.SimpleMaxFlow()

    for worker in fn.workers_nodes:
        graph.AddArcWithCapacity(fn.source, worker, 1)

    for i in range(len(fn.workers)):
        for j in range(len(fn.tasks)):
            if fn.costs[i][j] is True:
                graph.AddArcWithCapacity(
                    fn.workers_nodes[i], fn.tasks_nodes[j], 1
                )

    for task in fn.tasks_nodes:
        graph.AddArcWithCapacity(task, fn.sink, 1)

    solution = graph.Solve(fn.source, fn.sink)

    if solution == graph.OPTIMAL:
        assignment = Calculation(CalcType.SIMPLE, fn, graph).parse_solution()
        return make_response(assignment, 200)
    elif solution == graph.POSSIBLE_OVERFLOW:
        return make_response({}, 416)
    else:
        return make_response({}, 400)
