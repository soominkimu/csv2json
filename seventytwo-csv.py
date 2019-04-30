"""
Three columns CSV to JSON converter
"""
import csv

def isLast(itr):
    old = next(itr)
    for new in itr:
        yield False, old
        old = new
    yield True, old

with open('misc-data/seventytwo-names.csv', 'r', encoding='utf-8') as cf:
    in_data = csv.reader(cf, delimiter=',')
    # num_rows = sum(1 for row in in_data)
    print('{"s72":[', end='')
    for i, (is_last, row) in enumerate(isLast(in_data)):
        if (not row[0]):
            continue
        if (i % 3 == 0):
            print('[', end='')
        print('["'+row[0]+'","'+row[1]+'","'+row[2]+'"', end='')
        print(']', end='')
        if (i % 3 == 2):
            print(']', end='')
        if not is_last:
            print(',')
    print(']}')
#    print(nRow, 'data')
