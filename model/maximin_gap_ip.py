import operator
from typing import List, Tuple

import pulp
from pulp import PULP_CBC_CMD

from model.abstract_model import AbstractModel


class MaximinGapIp(AbstractModel):
    def __init__(self, interval_list: List[Tuple[int, int]]):
        self.m = pulp.LpProblem('Maximin Gap', pulp.LpMaximize)
        self.interval_list = interval_list
        self.length = len(interval_list)
        self.big_m = (max(interval_list, key=operator.itemgetter(1))[1] - min(
            interval_list, key=operator.itemgetter(0))[0]) * 2
        return

    def _set_iterables(self):
        self.n = list(range(self.length))
        self.arcs = [(i, j) for i in self.n for j in self.n if i > j]
        return

    def _set_variables(self):
        self.x = pulp.LpVariable.dicts('x',
                                       self.n,
                                       cat=pulp.LpContinuous,
                                       lowBound=0)
        self.y = pulp.LpVariable('y', cat=pulp.LpContinuous, lowBound=0)
        self.z = pulp.LpVariable.dicts('z', self.arcs, cat=pulp.LpBinary)
        return

    def _set_objective(self):
        self.m += pulp.lpSum(self.y)
        return

    def _set_constraints(self):
        for i in self.n:
            self.m += (self.x[i] >= self.interval_list[i][0], f'lb_{i}')
            self.m += (self.x[i] <= self.interval_list[i][1], f'up_{i}')
        for (i, j) in self.arcs:
            self.m += (self.x[i] >= self.x[j] + self.big_m *
                       (self.z[i, j] - 1), f'abs_0_{i}_{j}')
            self.m += (self.x[i] <= self.x[j] + self.big_m * self.z[i, j],
                       f'abs_1_{i}_{j}')
            self.m += (self.y <= self.x[i] - self.x[j] + self.big_m *
                       (1 - self.z[i, j]), f'abs_2_{i}_{j}')
            self.m += (self.y <=
                       self.x[j] - self.x[i] + self.big_m * self.z[i, j],
                       f'abs_3_{i}_{j}')
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
        self.m.writeLP('test.lp')
        return

    def _is_feasible(self):
        return True


if __name__ == '__main__':
    interval_list = [(0, 5), (3, 8), (1, 10)]
    model = MaximinGapIp(interval_list)
    result, gap = model.solve()
    print(result)
    print(gap)
