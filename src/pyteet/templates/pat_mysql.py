from pyteet.database import database

NAME = '{name}'

def migrate():
    db = database()
    sql = '''
        CREATE TABLE pyteet_pat (
            id bigint unsigned NOT NULL AUTO_INCREMENT,
            tokenable_module varchar(255) NOT NULL,
            tokenable_class varchar(255) NOT NULL,
            tokenable_id bigint unsigned NOT NULL,
            name varchar(255) NOT NULL,
            token varchar(255) NOT NULL,
            abilities varchar(255) NOT NULL,
            last_used_at timestamp NULL DEFAULT NULL,
            created_at timestamp NULL DEFAULT NULL,
            updated_at timestamp NULL DEFAULT NULL,
            PRIMARY KEY (id)
        )
    '''
    db.execute(sql)

def rollback():
    db = database()
    sql = '''
        DROP TABLE pyteet_pat
    '''
    db.execute(sql)

