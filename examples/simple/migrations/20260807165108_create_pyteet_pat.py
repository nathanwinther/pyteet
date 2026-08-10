from pyteet.database import database

NAME = '20260807165108_create_pyteet_pat'

def migrate():
    db = database()
    sql = '''
        CREATE TABLE pyteet_pat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tokenable_module TEXT NOT NULL,
            tokenable_class TEXT NOT NULL,
            tokenable_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            token TEXT NOT NULL,
            abilities TEXT NOT NULL,
            last_used_at TEXT NULL,
            created_at TEXT NULL,
            updated_at TEXT NULL
        )
    '''
    db.execute(sql)

def rollback():
    db = database()
    sql = '''
        DROP TABLE pyteet_pat
    '''
    db.execute(sql)
