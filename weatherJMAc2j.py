# CSV to JSON converter for Japanese Meteoroogical Agency data
# Extracts single column from the multi-column CSV data
# and save with meta data to a JSON file
# Soomin K. Dec.12,2018
# <F9> to run this python file in vim editor (need to set :nnoremap)

import csv
import json
import os
import sys

'''
Downloaded data's 'csvName shoud be in the format:
観測地点（都市名）-期間（始まりの年、10年単位、特に制約は無し）
Output JSON filename will be:
location-item-year, for example,
tokyo-Avg-2001.json

国土交通省気象庁　過去のデータ・ダウンロード
https://www.data.jma.go.jp/gmd/risk/obsdl/index.php
-----------------------------------------------
計測項目                       Name        col  Occurrences
-----------------------------------------------
最高気温(℃)                    Max           1
最低気温(℃)                    Min           6
平均気温(℃)                    Avg          11
降水量の合計(mm)               Rain         14  31.3%
日照時間(時間)                 SolarTime    18
合計全天日射量(MJ/㎡)          SolarEnergy  22
最深積雪(cm)                   Snow         25   0.5%
平均風速(m/s)                  Wind         36
平均湿度(％)                   Humidity     39
平均雲量(10分比)               Cloud        42
天気概況(昼：06時～18時)       StatusDay    45
天気概況(夜：18時～翌日06時)   StatusNight  48
-----------------------------------------------

Required Files (downloaded from 気象庁JMA)
-----------------------------------------------
|-- weatherJMAc2j.py
|
|-- dataCSV/
|    |-- tokyo-1991.csv
|    |-- tokyo-2001.csv
|    |-- tokyo-2011.csv
|
|-- dataJSON/
|    |-- tokyo-Avg-2001.json
|    |-- tokyo-c-2001.json
|
-----------------------------------------------

Compact daily weather status format
Max|Min|Avg|Rain|SolarTime|SolarEnergy|Snow|Wind|Humidity|Cloud|StatusDay|StatusNight
8.4|4.1|5.9||1.5|5.36||2.5|52|6.3|曇後晴|快晴, (~60 bytes/day) * 365 days ~ 21KB/year
* Date is not needed since all data should start for the Jan. 1, of the year and in sequence.

Further enhancements in data compression
----------------------------------------
Make a hash table and index for the Status fields (Day and Night).
There are 423 unique comments for the data 1991~2018 (10,206 days). 4.1%
-> Actually, most of the comments are shorter than the index itself (ex. 晴),
   then indexing cannot be effective.

For data with rare occurrences (Rain and Snow):
YYYYMMDD|NNN, (NNN positive for Rain, negative for Snow)

TIPS
----
# To check the sum of file sizes
$ ls -l tokyo-c-* | awk '{total += $5} END {print total/1024, "KB"}'
$ ls -l tokyo-c-* | wc | awk '{print $1, "files"}'
'''
class Deco:
    error     = '⚠️ '
    startIcon = '🌦 '
    csvIcon   = '🌡'
    colIcon   = '📚'
    rowIcon   = '📕'
    yearIcon  = '☀️'
    success   = 'SUCCESS!💋'
    sizeHeadC = '.....................................................>'
    sizeHeadR = '----------------------------------------------------->'
    totalHead = '==>'

def handleFileNotFoundError(f):
    print(Deco.error, f, ' not found!')
    sys.exit()

class PathName:   # directory names for the data files
    csv  = 'dataCSV/'
    json = 'dataJSON/'

if not os.path.exists(PathName.csv) or  \
   not os.path.exists(PathName.json):
    handleFileNotFoundError(PathName.csv + ' or ' + PathName.json)

# List of downloaded CSV filenames (http://bit.ly/2Lh4qzF)
csvFileList = []
################
try:
    csvFileList = [f for f in os.listdir(PathName.csv) \
                     if os.path.isfile(PathName.csv + f) and not f.startswith('.')]
except FileNotFoundError:
    handleFileNotFoundError(PathName.csv)

# Column names to be extracted
colName = [ \
    'Date', \
    'Max',         None, None, None, None, \
    'Min',         None, None, None, None, \
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

# colExtractList = [1,6,11,14,18,22,25,36,39,42,45,48]
colExtractList = []  # automatically build the list of columns to be extracted
###################
for cx in range(1, len(colName)):  # exclude the 'Date' column at the index 0
    if colName[cx] is not None:
        colExtractList.append(cx)

def getKB(size):
    return str(round(size/1024, 1)) + ' KB'

def getYears(days):
    return str(round(days/365.25, 2)) + ' years'


#######################################################################
## Main Module
def JMAMain(csvName):
    # Metadata in the output JSON file
    fname  = (csvName.split('.'))[0].split('-')
    locDF  = fname[0]  # location Data from Filename
    yearDF = fname[1]  # year Data from Filename

    class Ext:
        temp = 'temp'
        json = 'json'

    def getColName(col):
        return colName[colExtractList[col]]

    def getCsvPath():
        return PathName.csv + csvName

    def getFullPathOut(itemName, year=yearDF):
        return PathName.json + locDF    + '-' \
                             + itemName + '-' \
                             + year     + '.' \
                             + Ext.json

    def isCompactFormat(itemName):
        return itemName == 'c'

    def filter0(v):   ## nullify '0'
        return '' if v == '0' else v

    ###### Data store per column
    colDataList = []      # two-dimensional array
    for c in range(len(colExtractList)):
        colDataList.append([])

    ###### Data store per date
    rowDataList = []      # two-dimmensional array (per year)
    yearsList = []

    def WriteListJson(itemName, dataList, year=yearDF):
        fnJson = getFullPathOut(itemName, year)
        # Create a temp file to remove all the quotation characters in the JSON file
        ''' Unwanted quotation marks added when json.dump was called.
        Since I couldn't find easy way to prevent this behavior added a post process after dumping.
        Dump a temporary Json file and then apply some filters.  '''
        fnTemp = fnJson + '.' + Ext.temp
        try:
            with open(fnTemp, 'w') as tf:
                json.dump(dataList, tf, ensure_ascii=False, separators=(',', ':'))
            with open(fnTemp, 'r') as tf:
                outData = tf.readline().replace('"', '')
                # if isCompactFormat(itemName):
                #    outData = outData.replace('|0|', '||')     # nullify 0
        except FileNotFoundError:
            handleFileNotFoundError(fnTemp)

        try:
            # Output the JSON file with the meta data
            with open(fnJson, 'w') as jf:
                jf.write('{"meta":{"location":"' + locDF    \
                              + '","item":"'     + itemName \
                              + '","year":'      + year     \
                              + '},\n')
                jf.write('"data":')
                jf.write(outData)
                jf.write('}')
        except FileNotFoundError:
            handleFileNotFoundError(fnJson)

        # Cleanup
        if os.path.exists(fnTemp):
            os.remove(fnTemp)
        else:
            print(fnTemp, ' - File not exist')

        szJson = os.path.getsize(fnJson)
        print(Deco.rowIcon if isCompactFormat(itemName) else Deco.colIcon, fnJson, \
              ' (', getKB(szJson), ')')  # ternary operator
        return szJson

    # Read CSV file
    print(Deco.csvIcon, ' Source CSV:', getCsvPath())
    daysJson = 0
    with open(getCsvPath(), 'r') as cf:
        inData = csv.reader(cf, delimiter=',')
        ''' Process CSV data
        1. Save to colDataList[c] per column (i.e. per item) for each daily data
        2. Save to rowDataList[y] every column per day combining to a compact form, per year list '''
        yrId = 0
        for row in inData:
            if '/' not in row[0]:   # skip header part (with no date)
                continue
            s = ''
            for c, cx in enumerate(colExtractList):
                colDataList[c].append(filter0(row[cx]))
                if c > 0:
                    s += '|'             # compact form delimiter
                if row[cx] is not '0':
                    s += row[cx]
            if row[0].endswith('/1/1'):  # start date of the year
                rowDataList.append([])   # initialize new rowData for the new year
                yearsList.append(row[0][:4])
                yrId += 1
                print(Deco.yearIcon, yearsList[len(yearsList)-1], end='')  # print out the year
            rowDataList[yrId-1].append(s)
            daysJson += 1
    print('->Total', daysJson, 'days (', getYears(daysJson), ')')

    szColJson = 0
    szRowJson = 0
    for col in range(len(colExtractList)):
        szColJson += WriteListJson(getColName(col), colDataList[col])
    print(Deco.sizeHeadC, getKB(szColJson), ' in total.')

    for y in range(len(yearsList)):
        szRowJson += WriteListJson('c', rowDataList[y], yearsList[y])  #'c' for compact format
    print(Deco.sizeHeadR, getKB(szRowJson), ' in total. ', Deco.success)

    return szColJson, szRowJson, daysJson   # construct a tuple

#######################################################################
print(Deco.startIcon, 'TMA Data - Column IDs to be extracted:', colExtractList, '(', len(colName), 'columns)')
szColTotal = 0
szRowTotal = 0
daysTotal  = 0
for fn in csvFileList:
    szC, szR, d = JMAMain(fn)
    szColTotal += szC
    szRowTotal += szR
    daysTotal  += d
## REPORT statistics
print(Deco.totalHead, 'Column-wise   data:', getKB(szColTotal), 'in total.')
print(Deco.totalHead, 'Daily compact data:', getKB(szRowTotal), 'in total.', \
      round(szRowTotal/daysTotal, 1), 'bytes/day (', \
      getKB(szRowTotal/(daysTotal/365.25)), '/year) in average.')
print(Deco.totalHead, daysTotal, ' days (', getYears(daysTotal), ') in total.')
