"""CSV to JSON utilities"""
# Soomin K., Dec, 2018
import os
class Deco:
    """Decorative icons and messages"""
    error     = '⚠️ '
    warning   = '🚨'
    startIcon = '🌦 '
    csvIcon   = '🌡'
    colIcon   = '📚'
    rowIcon   = '📕'
    yearIcon  = '☀️'
    LeapYear  = '🌔'
    NoLeap    = '🌘'
    success   = 'SUCCESS!💋'
    tabs      = '...........'
    sizeHeadC = '.....................................................>'
    sizeHeadR = '----------------------------------------------------->'
    totalHead = '==>'
    line_top  = '======================================================'
    line_bot  = '------------------------------------------------------'

class PathName:   # directory names for the data files
    csv  = 'dataCSV/'
    json = 'dataJSON/'

## Error handlers
def handleFileNotFoundError(f):
    print(Deco.error, f, ' not found!')
    sys.exit()

def handleCriticalError(msg):
    print(Deco.error, msg)
    sys.exit()

def file_size(size):
    if size < 1024:
        return str(size) + ' bytes'
    elif size < 1024*1024:
        return str(round(size/1024, 1)) + ' KB'
    elif size < 1024*1024*1024:
        return str(round(size/1024/1024, 3)) + ' MB'
    else:
        return str(round(size/1024/1024/1024, 3)) + ' GB'

def get_years(days):
    return str(round(days/365.25, 2)) + ' years'

def check_paths():
    if not os.path.exists(PathName.csv) or  \
       not os.path.exists(PathName.json):
        handleFileNotFoundError(PathName.csv + ' or ' + PathName.json)

def get_loc_year_csv(csv_name):
    """get location and from_year from the given csv filename"""
    fname  = (csv_name.split('.'))[0].split('-')
    return fname[0], fname[1]

def get_fullpath_json(location, item, from_year):
    return PathName.json + location  + '-' \
                         + item      + '-' \
                         + from_year + '.json'

def json_meta_obj(location, from_date, to_date, item):
    """JSON meta object for JMA weather data"""
    return '{"meta":{"location":"' + location  \
                    + '","from":"' + from_date \
                    + '","to":"'   + to_date   \
                    + '","item":"' + item      \
                    + '"},\n'

def json_data_obj(str_data):
    """JSON data object for JMA weather data"""
    return '"data":' + str_data + '}'
