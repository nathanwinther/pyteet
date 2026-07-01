from pyteet import Model

class Contact(Model):

    TABLE = 'contacts'
    PRIMARY_KEY = 'id'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'
    CONNECTION = None # Use default database connection

    _companies = False

    def companies(self):
        if self._companies != False:
            return self._companies
        from models.company import Company
        sql = '''
            SELECT
            *
            FROM contact_company cc
            INNER JOIN company co ON cc.company_id = co.id
            WHERE cc.contact_id = %s
        '''
        self._companies = Company().fetchall(sql, (self.id, ))
        return self._companies

    def for_api(self):
        data = self.copy()
        data['fullname'] = ' '.join([
            self.firstname.strip(),
            self.lastname.strip(),
            ]).strip()
        data['companies'] = self.companies()
        return super().for_api(data)
