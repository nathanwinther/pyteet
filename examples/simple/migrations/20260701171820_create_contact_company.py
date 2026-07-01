from pyteet import database

NAME = '20260701171820_create_contact_company'
CONNECTION = None # Use default database connection

def migrate():
    db = database(CONNECTION)
    sql = '''
        CREATE TABLE contact_company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contact_id INTEGER NOT NULL,
            company_id INTEGER NOT NULL
        )
    '''
    db.execute(sql)
    sql = '''
        CREATE INDEX contact_company_idx_contact ON contact_company(contact_id)
    '''
    db.execute(sql)
    sql = '''
        CREATE INDEX contact_company_idx_company ON contact_company(company_id)
    '''
    db.execute(sql)

def rollback():
    db = database(CONNECTION)
    sql = '''
        DROP TABLE contact_company
    '''
    db.execute(sql)
