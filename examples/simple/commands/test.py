from models.contact import Contact

import argparse
import json
from pyteet.command import Command

class Test(Command):

    NAME = 'test'
    DESC = 'Command description'

    def __call__(self, args: list | None=[]):
        parser = argparse.ArgumentParser(
                description=self.DESC,
                usage=self.NAME)
        parsed = parser.parse_args(args)

        email = 'hello@nathanwinther.info'
        sql = '''
            SELECT
                *
            FROM contacts
            WHERE email = %s
            LIMIT 1
        '''

        contact = Contact().fetchone(sql, (email, ))
        if contact:
            print('Found contact')
            print(json.dumps(contact.for_api(), indent=2))
        else:
            print('Create contact')
            contact = Contact()
            contact.fill({
                'email': email,
                'password': Contact.password_hash('password'),
                'firstname': 'Nathan',
                'lastname': 'Winther',
                })
            contact.save()
            print(json.dumps(contact.for_api(), indent=2))

