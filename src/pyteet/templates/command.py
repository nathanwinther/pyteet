import argparse

NAME = '{{ name }}'
DESC = 'Command description'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parsed = parser.parse_args(args)
    # @TODO Your code here

