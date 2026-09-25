from pyteet.database import database

NAME = '{name}'

def migrate():
    db = database()
    sql = '''
    '''
    db.execute(sql)

def rollback():
    db = database()
    sql = '''
    '''
    db.execute(sql)

