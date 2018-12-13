# CSV to JSON converter for Japanese Meteoroogical Agency data
# Soomin K. Dec.12,2018
# <F9> to run this python file in vim editor (need to set :nnoremap)

import csv
import json
import os

# Downloaded data's 'FILENAME shoud be in the format:
# 観測地点（都市名）-期間（10年単位で始まりの年）
# Output JSON filename will be:
# location-item-year, for example,
# tokyo-Avg-2001.json
FILENAME     = 'tokyo-2001'
numHeadlines = 6   # number of lines in the header
colExtract   = 25  # column index (0..) to extract

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

# Metadata in the output JSON file
# Filename should be in the format:
metaData = FILENAME.split('-')
itemName = colName[colExtract]

class Ext:
    csv  = 'csv'
    temp = 'temp'
    json = 'json'

def getFullPath(ext):
    return 'dataCSV/' + FILENAME + '.' + ext

def getFullPathOut():
    return 'dataJSON/' + metaData[0] + '-' + itemName + '-' + metaData[1] + '.' + Ext.json

colData = []

# Read CSV file
print('Input CSV file:', getFullPath(Ext.csv))
with open(getFullPath(Ext.csv), 'r') as cf:
    inData = csv.reader(cf, delimiter=',')
    lineCnt = 0
    for row in inData:
        if lineCnt >= numHeadlines:
            colData.append(row[colExtract])
        lineCnt += 1
        if lineCnt % 10 == 0:
            print('.', end='')

print(lineCnt, 'lines read')

# Create a temp file to remove all the quotation characters in the JSON file
with open(getFullPath(Ext.temp), 'w') as tf:
    json.dump(colData, tf, ensure_ascii=False, separators=(',', ':'))

with open(getFullPath(Ext.temp), 'r') as tf:
    outData = tf.readline().replace('"', '')

# Output the JSON file with the meta data
print('Output JSON file:', getFullPathOut())
with open(getFullPathOut(), 'w') as jf:
    jf.write('{"meta":{"location":"' + metaData[0] \
                  + '","item":"'     + itemName \
                  + '","year":'      + metaData[1] \
                  + '},\n')
    jf.write('"data":')
    jf.write(outData)
    jf.write('}')

print('SUCCESS!')

# Cleanup
if os.path.exists(getFullPath(Ext.temp)):
    os.remove(getFullPath(Ext.temp))
else:
    print(getFullPath(Ext.temp), ' - File not exist')

