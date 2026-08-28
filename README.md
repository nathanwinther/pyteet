# Pyteet

A petite [WSGI](https://wsgi.readthedocs.io/)
web application framework. 
A simple wrapper around 
[Werkzeug](https://werkzeug.palletsprojects.com/)
Inspired by
[Laravel](https://laravel.com).

## Table of Contents

- [Install](#install)
- [Optional Requirements](#optional-requirements)
- [Dev Server](#dev-server)
- [License](#license)

## Install

```console
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pyteet
python3 -m pyteet init
```

## Optional Requirements

If you want to use `Model` with `mysql` or `postgresql`, add the following:

```console
python3 -m pip install -r mysql-connector-python
python3 -m pip install -r psycopg[binary]
```

## Dev Server

Run development server

```console
python3 -m app
```

## License

`pyteet` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
