from pyteet import database

NAME = '20260701171754_create_contacts'
CONNECTION = None # Use default database connection

def migrate():
    db = database(CONNECTION)
    sql = '''
        CREATE TABLE contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            created_at TEXT NULL,
            updated_at TEXT NULL
        )
    '''
    db.execute(sql)
    sql = '''
        CREATE INDEX contacts_idx_email ON contacts(email)
    '''
    db.execute(sql)

def rollback():
    db = database(CONNECTION)
    sql = '''
        DROP TABLE contacts
    '''
    db.execute(sql)
