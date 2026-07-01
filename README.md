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

## About

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

## License

`pyteet` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
