# CSV to JSON utilities

# Soomin K., Dec, 2018

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
