# pyteet

Pyteet is a lightweight [WSGI](https://wsgi.readthedocs.io/)
web application framework. It is a simple wrapper around 
[Werkzeug](https://werkzeug.palletsprojects.com/) and 
[Jinja](https://jinja.palletsprojects.com/) inspired by
[Laravel](https://laravel.com).

## Table of Contents

- [Installation](#installation)
- [Commands](#commands)
- [License](#license)

## Installation

```console
python3 -m pip install pyteet
```

## Commands

View available commands

```console
python3 -m pyteet
```

Set up a new project

```console
python3 -m pyteet init
cp app.ini.example app.ini
```

Create your own commands

```console
python3 -m pyteet make command orders
```

Create a controller

```console
python3 -m pyteet make controller contact
```

Create a model

```console
python3 -m pyteet make model Contact
```

Create a database migration

```console
python3 -m pyteet make migration create_contacts
```

View database migrations

```console
python3 -m pyteet migrate status
```

Run database migrations

```console
python3 -m pyteet migrate run
```

Rollback database migrations

```console
python3 -m pyteet migrate rollback
```

## License

`pyteet` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
