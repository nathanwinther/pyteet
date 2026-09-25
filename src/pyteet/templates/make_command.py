import argparse
from pyteet.command import Command

class {name}(Command):

    NAME = '{snake}'
    DESC = 'Command description'

    def __call__(self, args: list | None=[]):
        parser = argparse.ArgumentParser(
                description=self.DESC,
                usage=self.NAME)
        parsed = parser.parse_args(args)

        # @TODO Your code here

