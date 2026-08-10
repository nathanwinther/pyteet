from pyteet.database import database

NAME = '20260807165136_contacts'

def migrate():
    db = database()
    sql = '''
        CREATE TABLE contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            last_login TEXT NULL,
            created_at TEXT NULL,
            updated_at TEXT NULL
        )
    '''
    db.execute(sql)
    sql = '''
        CREATE UNIQUE INDEX contacts_idx_email ON contacts(email)
    '''
    db.execute(sql)

def rollback():
    db = database()
    sql = '''
        DROP TABLE contacts
    '''
    db.execute(sql)
