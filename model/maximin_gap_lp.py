from typing import List, Tuple

import pulp
from pulp import PULP_CBC_CMD

from model.abstract_model import AbstractModel


class MaximinGapLp(AbstractModel):
    def __init__(self, interval_list: List[Tuple[int, int]]):
        self.m = pulp.LpProblem('Maximin Gap', pulp.LpMaximize)
        self.interval_list = interval_list
        self.length = len(interval_list)
        return

    def _set_iterables(self):
        self.n = list(range(self.length))
        self.n_prime = list(range(1, self.length))
        return

    def _set_variables(self):
        self.x = pulp.LpVariable.dicts('x', self.n, cat=pulp.LpContinuous, lowBound=0)
        self.y = pulp.LpVariable('y', cat=pulp.LpContinuous, lowBound=0)
        return

    def _set_objective(self):
        self.m += pulp.lpSum(self.y)
        return

    def _set_constraints(self):
        for i in self.n:
            self.m += (self.x[i] >= self.interval_list[i][0], f'lb_{i}')
            self.m += (self.x[i] <= self.interval_list[i][1], f'up_{i}')
        for i in self.n_prime:
            self.m += (self.y <= self.x[i] - self.x[i-1], f'gap_{i}')
        return

    def _post_process(self):
        result = [self.x[i].value() for i in self.n]
        gap = self.y.value()
        return result, gap

    def _process_infeasible_case(self):
        return list(), float('infty')

    def _optimize(self):
        time_limit_in_seconds = 60 * 60
        self.m.solve(PULP_CBC_CMD(msg=1, timeLimit=time_limit_in_seconds))
        return

    def _is_feasible(self):
        return True


if __name__ == '__main__':
    interval_list = [(0, 5), (3, 8), (1, 10)]
    model = MaximinGapLp(interval_list)
    result, gap = model.solve()
    print(result)
    print(gap)
