import numpy as np
from ortools.graph import pywrapgraph
from .calc_type import CalcType
from .flow_network import FlowNetwork


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
