from model.maximin_gap import MaximinGap


def main():
    interval_list = [(0, 5), (3, 8), (1, 10)]
    model = MaximinGap(interval_list)
    result, gap = model.solve()
    print(result)
    print(gap)
    return


if __name__ == '__main__':
    main()
