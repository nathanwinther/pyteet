import hashlib
from datetime import datetime
from datetime import UTC
from pyteet.model import Model
from pyteet.database import DATETIME

class Contact(Model):

    TABLE = 'contacts'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    @staticmethod
    def login(email: str, password: str) -> Contact:
        sql = '''
            SELECT
                *
            FROM contacts
            WHERE email = %s
            AND password = %s
            LIMIT 1
        '''
        inst = Contact().fetchone(sql, (
            email, 
            Contact.password_hash(password)))
        if inst:
            inst.last_login = datetime.now(UTC).strftime(DATETIME)
            inst.save()
        return inst

    def for_api(self):
        data = self.data()
        if 'password' in data:
            del(data['password'])
        data['fullname'] = ' '.join([
            data.get('firstname', '').strip(),
            data.get('lastname', '').strip(),
            ]).strip()
        return super().for_api(data)

    @staticmethod
    def password_hash(string: str) -> str:
        return hashlib.md5(string.encode('utf-8')).hexdigest()

