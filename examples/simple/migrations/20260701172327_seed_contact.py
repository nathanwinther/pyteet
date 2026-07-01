from pyteet import database

NAME = '20260701172327_seed_contact'
CONNECTION = None # Use default database connection

def migrate():
    db = database(CONNECTION)
    sql = '''
        INSERT INTO contacts (email, firstname, lastname, created_at, updated_at)
        VALUES(
            'nathanwinther@fastmail.fm',
            'Nathan',
            'Winther',
            datetime('now'),
            datetime('now')
        )
    '''
    contact_id = db.insert(sql)
    sql = '''
        INSERT INTO company (name, created_at, updated_at)
        VALUES('ABC Bakery', datetime('now'), datetime('now'))
    '''
    company_id = db.insert(sql)
    sql = '''
        INSERT INTO contact_company(contact_id, company_id)
        VALUES(%s, %s)
    '''
    db.execute(sql, (contact_id, company_id))
    sql = '''
        INSERT INTO company (name, created_at, updated_at)
        VALUES('XYZ Industries', datetime('now'), datetime('now'))
    '''
    company_id = db.insert(sql)
    sql = '''
        INSERT INTO contact_company(contact_id, company_id)
        VALUES(%s, %s)
    '''
    db.execute(sql, (contact_id, company_id))

def rollback():
    pass
