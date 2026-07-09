from pyteet import database

NAME = '{{ prefix }}_create_pyteet_pat'
CONNECTION = None # Use default database connection

def migrate():
    db = database(CONNECTION)
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
    db = database(CONNECTION)
    sql = '''
        DROP TABLE pyteet_pat
    '''
    db.execute(sql)
