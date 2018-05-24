import datetime
from enum import IntEnum
import numpy as np
from ortools.graph import pywrapgraph


class CalcType(IntEnum):
    SUM = 1
    SUM_MAX = 2
    BOTTLENECK = 3
    SIMPLE = 4


class FlowNetwork:
    def __init__(self, workers, tasks, costs):
        self.workers = workers
        self.tasks = tasks
        self.costs = costs

        self.source = 0
        self.sink = len(workers) + len(tasks) + 1
        self.workers_nodes = list(range(1, len(workers) + 1))
        self.tasks_nodes = list(range(len(workers) + 1, self.sink))

        self.max_cost = 0

    def get_task_name(self, node_index):
        return self.tasks[self.tasks_nodes.index(node_index)]

    def get_worker_name(self, node_index):
        return self.workers[self.workers_nodes.index(node_index)]

    def prepare_costs_for_max(self):
        np_costs = np.array(self.costs, dtype=np.float)
        self.max_cost = int(np.nanmax(list(map(np.nanmax, np_costs))))

        for i in range(len(self.workers)):
            for j in range(len(self.tasks)):
                if self.costs[i][j] is not None:
                    self.costs[i][j] = self.max_cost - self.costs[i][j]


class Calculation:
    def __init__(self, calc_type: CalcType, fn: FlowNetwork, graph):
        self.type = calc_type
        self.fn = fn
        self.graph = graph

    def parse_solution(self):
        assignment = []
        result = self.get_calculation_result()

        for arc in range(self.graph.NumArcs()):
            if (
                self.graph.Tail(arc) != self.fn.source
                and self.graph.Head(arc) != self.fn.sink
            ):
                if self.graph.Flow(arc) > 0:
                    value = self.get_single_assignment_cost(arc)
                    if self.type == CalcType.SUM_MAX:
                        result += value

                    worker_node = self.graph.Tail(arc)
                    task_node = self.graph.Head(arc)

                    assignment.append({
                        'worker': self.fn.get_worker_name(worker_node),
                        'task': self.fn.get_task_name(task_node),
                        'value': value,
                        'row': self.fn.workers_nodes.index(worker_node) + 1,
                        'col': self.fn.tasks_nodes.index(task_node) + 1
                    })

        return {
            'type': self.type,
            'assignment': assignment,
            'numResult': result
        }

    def get_calculation_result(self):
        if self.type == CalcType.SIMPLE:
            return self.graph.OptimalFlow()
        elif self.type == CalcType.SUM:
            return self.graph.OptimalCost()
        else:
            return 0

    def get_single_assignment_cost(self, arc):
        if self.type == CalcType.SIMPLE:
            return 0
        elif self.type == CalcType.SUM_MAX:
            return self.fn.max_cost - self.graph.UnitCost(arc)
        else:
            return self.graph.UnitCost(arc)


def make_response(response, status):
    response['status'] = status

    if status == 200:
        msg = 'Obliczenia zakończone sukcesem!'
    elif status == 400:
        msg = 'Przydział dla wprowadzonych danych nie jest możliwy.'
    elif status == 416:
        msg = (
            'Niektóre wartości kosztów są zbyt wysokie i mogą '
            'spowodować przekroczenie zakresu liczb całkowitych.'
        )
    elif status == 500:
        msg = 'Wystąpił wewnętrzny błąd serwera.'
    elif status == 501:
        msg = 'Nie znaleziono określonego typu obliczeń.'

    response['message'] = msg
    response['calculationDate'] = datetime.datetime.now().isoformat()
    return response
