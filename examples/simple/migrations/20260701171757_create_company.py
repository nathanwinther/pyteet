from pyteet import database

NAME = '20260701171757_create_company'
CONNECTION = None # Use default database connection

def migrate():
    db = database(CONNECTION)
    sql = '''
        CREATE TABLE company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NULL,
            updated_at TEXT NULL
        )
    '''
    db.execute(sql)
    sql = '''
        CREATE INDEX company_idx_name ON company(name)
    '''
    db.execute(sql)

def rollback():
    db = database(CONNECTION)
    sql = '''
        DROP TABLE company
    '''
    db.execute(sql)
