# CSV to JSON converter for Japanese Meteoroogical Agency data
# Extracts single column from the multi-column CSV data
# and save with meta data to a JSON file
# Soomin K. Dec.12,2018
# <F9> to run this python file in vim editor (need to set :nnoremap)

import csv
import json
import os

# Downloaded data's 'csvName shoud be in the format:
# 観測地点（都市名）-期間（始まりの年、10年単位、特に制約は無し）
# Output JSON filename will be:
# location-item-year, for example,
# tokyo-Avg-2001.json

# 国土交通省気象庁　過去のデータ・ダウンロード
# https://www.data.jma.go.jp/gmd/risk/obsdl/index.php
# -----------------------------------------------
# 計測項目                       Name        col
# -----------------------------------------------
# 最高気温(℃)                    Max           1
# 最低気温(℃)                    Min           6
# 平均気温(℃)                    Avg          11
# 降水量の合計(mm)               Rain         14
# 日照時間(時間)                 SolarTime    18
# 合計全天日射量(MJ/㎡)          SolarEnergy  22
# 最深積雪(cm)                   Snow         25
# 平均風速(m/s)                  Wind         36
# 平均湿度(％)                   Humidity     39
# 平均雲量(10分比)               Cloud        42
# 天気概況(昼：06時～18時)       StatusDay    45
# 天気概況(夜：18時～翌日06時)   StatusNight  48
# -----------------------------------------------

# Required Files (downloaded from 気象庁JMA)
# -----------------------------------------------
# |-- weatherJMAc2j.py
# |
# |-- dataCSV/
# |    |-- tokyo-1991.csv
# |    |-- tokyo-2001.csv
# |    |-- tokyo-2011.csv
# |
# |-- dataJSON/
# |    |-- tokyo-Avg-2001.json
# |
# -----------------------------------------------

csvNameList = [ \
    'tokyo-1991', \
    'tokyo-2001', \
    'tokyo-2011', \
    ]
colExtractList = [1,6,11,14,18,22,25,36,39,42,45,48]
colName = [ \
    'Date', \
    'Max',         None, 'time', None, None, \
    'Min',         None, 'time', None, None, \
    'Avg',         None, None, \
    'Rain',        None, None, None, \
    'SolarTime',   None, None, None, \
    'SolarEnergy', None, None,  \
    'Snow',        None, None, None, None, None, None, None, None, None, None, \
    'Wind',        None, None, \
    'Humidity',    None, None, \
    'Cloud',       None, None, \
    'StatusDay',   None, None, \
    'StatusNight', None, None]

def JMAMain(csvName):
    numHeadlines = 6   # number of lines in the header (csv file)

    # Metadata in the output JSON file
    # Filename should be in the format:
    metaData = csvName.split('-')

    class Ext:
        csv  = 'csv'
        temp = 'temp'
        json = 'json'

    def getColName(col):
        return colName[colExtractList[col]]

    def getFullPath(ext):
        return 'dataCSV/' + csvName + '.' + ext

    def getFullPathOut(col, ext):
        return 'dataJSON/' + metaData[0]     + '-' \
                           + getColName(col) + '-' \
                           + metaData[1]     + '.' \
                           + ext

    colDataList = []      # two-dimensional list
    for c in colExtractList:
        colDataList.append([])

    # Read CSV file
    fname = getFullPath(Ext.csv)
    print('● Source CSV:', fname, ' ', end='')
    with open(fname, 'r') as cf:
        inData = csv.reader(cf, delimiter=',')
        lineCnt = 0
        for row in inData:
            if lineCnt >= numHeadlines:
                for c in range(0, len(colExtractList)):
                    colDataList[c].append(row[colExtractList[c]])
            lineCnt += 1
            if lineCnt % 365 == 0:
                print('.', end='')
    print(lineCnt, 'lines read')

    for col in range(0, len(colExtractList)):
        # Create a temp file to remove all the quotation characters in the JSON file
        fname = getFullPathOut(col, Ext.temp)
        with open(fname, 'w') as tf:
            json.dump(colDataList[col], tf, ensure_ascii=False, separators=(',', ':'))

        with open(fname, 'r') as tf:
            outData = tf.readline().replace('"', '')

        # Output the JSON file with the meta data
        fname = getFullPathOut(col, Ext.json)
        print('->', fname)
        with open(fname, 'w') as jf:
            jf.write('{"meta":{"location":"' + metaData[0] \
                          + '","item":"'     + getColName(col) \
                          + '","year":'      + metaData[1] \
                          + '},\n')
            jf.write('"data":')
            jf.write(outData)
            jf.write('}')

        # Cleanup
        fname = getFullPathOut(col, Ext.temp)
        if os.path.exists(fname):
            os.remove(fname)
        else:
            print(fname, ' - File not exist')

    print('SUCCESS!')

# csvName   : 'tokyo-2001'
# colExtract: # column index (0..) to extract
print('# of columns:', len(colName))
for fn in csvNameList:
    JMAMain(fn)
