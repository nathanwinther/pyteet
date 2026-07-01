from pyteet import config

import argparse

NAME = 'env'
DESC = 'Print app.env'

def run(args):
    parser = argparse.ArgumentParser(
            description=DESC,
            usage=NAME)
    parsed = parser.parse_args(args)
    print(config('app.env'))
