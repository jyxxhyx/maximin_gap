import itertools
import operator
from random import random, randint

from model.maximin_gap_lp import MaximinGapLp
from model.maximin_gap_ip import MaximinGapIp
from output_handler.drawer import draw_result
from output_handler.writer import output_file


def main():
    n = 50
    interval_list = _generate_random_intervals(n)
    if _check_subset(interval_list):
        # 不存在包含关系，则对interval_list重新排序
        interval_list.sort(key=operator.itemgetter(0))
        model = MaximinGapLp(interval_list)
        print('Solving the problem via LP.')
    else:
        model = MaximinGapIp(interval_list)
        print('Solving the problem via IP.')
    result, gap = model.solve()
    output_file(interval_list, result, gap, 'maximin_gap.txt')
    draw_result(interval_list, result, 'maximin_gap')
    return


def _generate_random_intervals(length: int):
    temp = [(randint(0, 1000), randint(5, 100)) for _ in range(length)]
    return [(a, a + b) for (a, b) in temp]


def _check_subset(intervals):
    """
    检查区间是否是包含关系
    如果不存在包含关系，用LP模型求解；
    如果存在包含关系，则用IP模型求解。
    :param intervals:
    :return:
    """
    for interval1, interval2 in itertools.permutations(intervals, r=2):
        if interval1[0] <= interval2[0] and interval1[1] >= interval2[1]:
            if interval1[0] != interval2[0] or interval1[1] != interval1[1]:
                return False
    return True


if __name__ == '__main__':
    main()
