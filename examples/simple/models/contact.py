import hashlib
from datetime import datetime, UTC
from pyteet import DATETIME, Model

class Contact(Model):

    TABLE = 'contacts'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    def for_api(self):
        data = self.copy()
        del(data['password'])
        data['fullname'] = ' '.join([
            self.firstname.strip(),
            self.lastname.strip(),
            ]).strip()
        return super().for_api(data)

    @staticmethod
    def login(email: str, password: str) -> Contact:
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        sql = '''
            SELECT
                *
            FROM contacts
            WHERE email = %s
            AND password = %s
            LIMIT 1
        '''
        inst = Contact().fetchone(sql, (email, password))
        if not inst:
            return None
        inst.last_login = datetime.now(UTC).strftime(DATETIME)
        inst.save()
        return inst

    def saving(self):
        if 'password' in self._dirty:
            self.password = hashlib.md5(
                    self.password.encode('utf-8')).hexdigest()

