from pyteet import database

NAME = '{{ name }}'
CONNECTION = None # Use default database connection

def migrate():
    db = database(CONNECTION)
    sql = '''
    '''
    db.execute(sql)

def rollback():
    db = database(CONNECTION)
    sql = '''
    '''
    db.execute(sql)

