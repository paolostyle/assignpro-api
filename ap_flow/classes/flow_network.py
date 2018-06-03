import numpy as np


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
