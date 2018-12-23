#!/usr/bin/env python3
# CSV to JSON converter for Japanese Meteorological Agency data
# Extracts single column from the multi-column CSV data
# and save with meta data to a JSON file
# Soomin K. Dec.12,2018
# <F9> to run this python file in vim editor (need to set :nnoremap)
# Repo: https://github.com/soominkimu/csv2json

'''
# Google Python Style Guide: https://google.github.io/styleguide/pyguide.html (snake_case)
  module_name,       package_name,            ClassName,        method_name, ExceptionName,
  function_name,     GLOBAL_CONSTANT_NAME,    global_var_name,
  instance_var_name, function_parameter_name, local_var_name

Downloaded data's csv filename shoud be in the format:
    観測地点（都市名）-期間（始まりの年、10年単位、特に制約は無し）
Output JSON filename will be in the format:
    location-item-year, for example,
    tokyo-Avg-2001.json

国土交通省気象庁　過去のデータ・ダウンロード
https://www.data.jma.go.jp/gmd/risk/obsdl/index.php
* Data 1875~
------------------------------------------
計測項目                       Name   col  Occurrences
------------------------------------------
最高気温(℃)                    Max      1
最低気温(℃)                    Min      6
平均気温(℃)                    Avg     11
降水量の合計(mm)               Rain    14  31.3%  * 0->null
.....................................................
日照時間(時間)                 SolarT  18  since 1961
合計全天日射量(MJ/㎡)          SolarE  22
最深積雪(cm)                   Snow    25   0.5%  * 0->null
平均風速(m/s)                  Wind    36
平均湿度(％)                   Humid   39
平均雲量(10分比)               Cloud   42
.....................................................
天気概況(昼：06時～18時)       StatD   45  since 1967/1/1
天気概況(夜：18時～翌日06時)   StatN   48
------------------------------------------
* 0->null: To save space, convert 0 to null

Required Files (downloaded from 気象庁JMA)
-----------------------------------------------
|-- weatherJMAc2j.py
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
Max|Min|Avg|Rain|SolarT|SolarE|Snow|Wind|Humid|Cloud|StatusD|StatusN
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
import csv
import json
import os
import calendar

import c2j_util as cj

if not os.path.exists(cj.PathName.csv) or  \
   not os.path.exists(cj.PathName.json):
    cj.handleFileNotFoundError(cj.PathName.csv + ' or ' + cj.PathName.json)

class CsvFile:
    """List of downloaded CSV filenames (http://bit.ly/2Lh4qzF)"""
    csv_list = []
    ##################
    def get_csv_list(self):
        return self.csv_list

    def __init__(self):
        try:
            self.csv_list = [f for f in os.listdir(cj.PathName.csv) \
                             if os.path.isfile(cj.PathName.csv + f) and not f.startswith('.')]
        except FileNotFoundError:
            cj.handleFileNotFoundError(cj.PathName.csv)
        self.csv_list.sort()

class ColInfo:
    """Column Information of the source CSV file"""
    # Column names to be extracted
    name = [ \
        'Date', \
    # following items that have names will be exported to JSON output
        'Max',     None, None, None, None, \
        'Min',     None, None, None, None, \
        'Avg',     None, None, \
        'Rain',    None, None, None, \
    # following items are available since 1961
        'SolarT',  None, None, None, \
        'SolarE',  None, None,  \
        'Snow',    None, None, None, None, None, None, None, None, None, None, \
        'Wind',    None, None, \
        'Humid',   None, None, \
        'Cloud',   None, None, \
        'StatusD', None, None, \
        'StatusN', None, None]

    # ext_list = [1,6,11,14,18,22,25,36,39,42,45,48]
    ext_list = []  # automatically build the list of columns to be extracted
    cnt_list = []  # keep the count of valid data in each column
    #####################
    def __init__(self):
        for cx in range(1, len(self.name)):  # exclude the 'Date' column at the index 0
            if self.name[cx] is not None:
                self.ext_list.append(cx)  # register the index of the column to be extracted
                self.cnt_list.append(0)       # initialize column data counts to 0

## Instantiate the main classes
CF = CsvFile()
CI = ColInfo()

#######################################################################
## Main Module
def jma_main(csv_name):
    # Metadata in the output JSON file
    fname  = (csv_name.split('.'))[0].split('-')
    locDF  = fname[0]  # location Data from Filename
    yrs_df = fname[1]  # year from Data Filename

    # slice for old data, since JMA has no meaningful data until 1961 except the first 4 items
    col_x_lst = CI.ext_list if int(yrs_df) > 1960 else CI.ext_list[:4]

    def get_fullpath_out(item_name, year=yrs_df):
        return cj.PathName.json + locDF  + '-' \
                             + item_name + '-' \
                             + year      + '.json'

    def is_compact(item_name):
        return item_name == 'c'

    def filter0(v, cx):     ## nullify '0' only for the columns
        if cx in [14, 25]:  ## Rain and Snow
            return '' if v == '0' else v
        else:
            return v

    def get_compact_items():
        s = ''
        for c, cx in enumerate(col_x_lst):
            if c > 0:
                s += '|'
            s += CI.name[cx]
        return s

    ###### Data store per column
    col_data_lst = []      # two-dimensional array
    for c in range(len(col_x_lst)):
        col_data_lst.append([])

    ###### Data store per date
    row_data_lst = []      # two-dimmensional array (per year)
    years_lst = []
    date_from = ''
    date_to   = ''

    def WriteListJson(item_name, data_lst, year=yrs_df):
        fn_json = get_fullpath_out(item_name, year)
        # Create a temp file to remove all the quotation characters in the JSON file
        ''' Unwanted quotation marks added when json.dump was called.
        Since I couldn't find easy way to prevent this behavior added a post process after dumping.
        Dump a temporary Json file and then apply some filters.  '''
        fn_tmp = fn_json + '.temp'
        try:
            with open(fn_tmp, 'w') as tf:
                json.dump(data_lst, tf, ensure_ascii=False, separators=(',', ':'))
            with open(fn_tmp, 'r') as tf:
                outData = tf.readline().replace('"', '')   # eliminate quotation mark
        except FileNotFoundError:
            cj.handleFileNotFoundError(fn_tmp)

        meta = '{"meta":{"location":"' + locDF   \
                     + '","from":"' + date_from  \
                     + '","to":"'   + date_to    \
                     + '","item":"' + (get_compact_items() if is_compact(item_name) else item_name) \
                     + '"},\n'

        try:
            # Output the JSON file with the meta data
            with open(fn_json, 'w') as jf:
                jf.write(meta)
                jf.write('"data":')
                jf.write(outData)
                jf.write('}')
        except FileNotFoundError:
            cj.handleFileNotFoundError(fn_json)

        # Cleanup
        if os.path.exists(fn_tmp):
            os.remove(fn_tmp)
        else:
            print(fn_tmp, ' - File not exist')

        sz_json = os.path.getsize(fn_json)    # ternary operator
        print(cj.Deco.rowIcon if is_compact(item_name) else cj.Deco.colIcon, \
              fn_json, ' (', cj.file_size(sz_json), ') ', end='')
        if is_compact(item_name):
            days_year = 366 if calendar.isleap(int(year)) else 365
            print(len(data_lst), 'days ', \
                  cj.Deco.LeapYear if (days_year == 366) else cj.Deco.NoLeap,  \
                  cj.Deco.warning + 'Incomplete data!' if (len(data_lst) != days_year) else '')
        else:
            print(cj.Deco.tabs, cj.get_years(len(data_lst)))
        return sz_json

    # Read CSV file
    print(cj.Deco.csvIcon, ' Data Source:', cj.PathName.csv + csv_name)
    days_count = 0
    try:
        with open(cj.PathName.csv + csv_name, 'r', encoding='utf-8') as cf:
            inData = csv.reader(cf, delimiter=',')
            ''' Process CSV data
            1. Save to col_data_lst[c] per column (i.e. per item) for each daily data
            2. Save to row_data_lst[y] every column per day combining to a compact form, per year list '''
            yrId = -1  # index for the yearly list
            for row in inData:
                if ('/' not in row[0]) or (not row[0][:4].isnumeric()):   # skip header part (that has no date)
                    continue
                s = ''
                date_to = row[0][:10]  # to save out of the loop, ex: 2018/12/20
                for c, cx in enumerate(col_x_lst):
                    if row[cx] != '':
                        CI.cnt_list[c] += 1
                    val = filter0(row[cx], cx)
                    col_data_lst[c].append(val)
                    if c > 0:
                        s += '|'             # compact form delimiter
                    if val is not '':
                        s += row[cx]
                if (days_count == 0) or (row[0].endswith('/1/1')):  # start date of the year
                    if (days_count == 0):
                        date_from = date_to
                    row_data_lst.append([])   # initialize new rowData for the new year
                    years_lst.append(date_to[:4])
                    yrId  += 1
                    print(cj.Deco.yearIcon, years_lst[len(years_lst)-1], end='')  # print out the year
                row_data_lst[yrId].append(s)
                days_count += 1
    except Unicodecj.Deco.eError:
        cj.handleCriticalError('Unicodecj.Deco.eError')
    print('->Total', days_count, 'days (', cj.get_years(days_count), ')')

    sz_col_j = 0
    sz_row_j = 0
    for col in range(len(col_x_lst)):
        if CI.cnt_list[col] > 0:
            sz_col_j += WriteListJson(CI.name[col_x_lst[col]], col_data_lst[col])
    print(cj.Deco.sizeHeadC, cj.file_size(sz_col_j), ' in total.')

    for y in range(len(years_lst)):
        sz_row_j += WriteListJson('c', row_data_lst[y], years_lst[y])  #'c' for compact format
    print(cj.Deco.sizeHeadR, cj.file_size(sz_row_j), ' in total. ', cj.Deco.success)

    return sz_col_j, sz_row_j, days_count   # construct a tuple

#######################################################################
print(cj.Deco.startIcon, 'TMA Data - Column IDs to be extracted:', CI.ext_list, '(', len(CI.name), 'columns)')
sz_col_total = 0
sz_row_total = 0
days_total   = 0
for fn in CF.get_csv_list():
    sz_c, sz_r, d = jma_main(fn)
    sz_col_total += sz_c
    sz_row_total += sz_r
    days_total   += d
## REPORT statistics
print(cj.Deco.totalHead, 'Column-wise   data:', cj.file_size(sz_col_total), 'in total.')
print(cj.Deco.totalHead, 'Daily compact data:', cj.file_size(sz_row_total), 'in total.', \
      round(sz_row_total/days_total, 1), 'bytes/day (', \
      cj.file_size(sz_row_total*365.25/days_total), '/year) in average.')
print(cj.Deco.totalHead, days_total, ' days (', cj.get_years(days_total), ') in total.')

## End of program
