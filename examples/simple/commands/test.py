from models.contact import Contact

import argparse
import json
from datetime import datetime
from pyteet.command import Command
from pyteet.jsonlogging import logger
from pyteet.utils import jsonify

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
            logger.info(f'Found contact for {email}')
            logger.debug(jsonify(contact.for_api()))
        else:
            logger.info('Create contact')
            contact = Contact()
            contact.fill({
                'email': email,
                'password': Contact.password_hash('password'),
                'firstname': 'Nathan',
                'lastname': 'Winther',
                })
            contact.save()
            contact = Contact().find(contact.id)
            logger.debug(jsonify(contact.for_api()))

