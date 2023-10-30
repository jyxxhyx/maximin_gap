

def output_file(interval_list, result, gap, file_name):
    with open(file=file_name, mode='w', encoding='utf-8') as f:
        f.write(f'Intervals: length\t{len(interval_list)}\r\n')
        for index, interval in enumerate(interval_list):
            f.write(f'{index},\t{interval[0]},\t{interval[1]}\r\n')
        f.write(f'Result: gap\t{gap}\r\n')
        for index, x in enumerate(result):
            f.write(f'{index}, \t{x}\r\n')
