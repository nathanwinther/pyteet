# pyteet

[![PyPI - Version](https://img.shields.io/pypi/v/pyteet.svg)](https://pypi.org/project/pyteet)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyteet.svg)](https://pypi.org/project/pyteet)

-----

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Commands](#commands)
- [License](#license)

## About

Pyteet is a lightweight [WSGI](https://wsgi.readthedocs.io/)
web application framework. It is a simple wrapper around 
[Werkzeug](https://werkzeug.palletsprojects.com/) and 
[Jinja](https://jinja.palletsprojects.com/) inspired by
[Laravel](https://laravel.com).

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
```

Create your own commands

```console
python3 -m pyteet make command orders
```

And then run you command

```console
python3 -m pyteet orders
```

## License

`pyteet` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
