from time import gmtime, strftime

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_time():
    raw_time = strftime("%Y/%m/%d %H:%M:%S", gmtime())
    return '[' + raw_time + '] '