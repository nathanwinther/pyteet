from pyteet import Model

class Company(Model):

    TABLE = 'company'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection
