import os

# project's status
DEBUG = True

# mail's config
MAIL = {
    'from'     : '',
    'password' : '',
    'to'       : [],
    'to_test'  : [],
    'smtp'     : ''
}

# sqlite3 data path
DATAPATH = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])+"/data/data.db"

# mysql's config
MYSQL = {
    'host'   : '',
    'user'   : '',
    'passwd' : '',
    'db'     : '',
    'charset': 'utf8'
}