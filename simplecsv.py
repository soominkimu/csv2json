"""
Simple single column CSV to JSON converter
"""
import csv

with open('misc-data/tokyo-2018.csv', 'r', encoding='utf-8') as cf:
    in_data = csv.reader(cf, delimiter=',')
    print('{"Avg":[', end='')
    nCnt = 0
    for row in in_data:
        if (not row[0]):
            continue
        if (nCnt > 0):
            print(',', end='')
        print(row[0], end='')
        nCnt += 1
    print(']}')
#    print(nCnt, 'data')
