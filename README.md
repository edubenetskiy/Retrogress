# Retrogress

A simple web-based RSS aggregator written in Python.

## Background

**R**etrogre**ss** is developed as the 6th assignment for the *Programming Technologies* course at [ITMO University].

## Install

```
pipenv install
```

An SQLite database should be created before first run.
Database schema can be found in the file file `database/schema.sql`.
Path to database file should be specified in the configuration key `DATABASE` in the file `config.py`.

## Usage

```
pipenv run python run.py
```

## Screenshots

<img alt="Screenshot of the home page" src="https://raw.githubusercontent.com/edubenetskiy/ProgTech-Lab6/master/screenshots/main-page.png" height="300px"> <img alt="Screenshot of a feed" src="https://raw.githubusercontent.com/edubenetskiy/ProgTech-Lab6/master/screenshots/sample-feed.png" height="300px">

## Contributing

Feel free to dive in! Open an issue or submit PRs.

## License

Licensed either under the terms of [Apache-2.0] or [MIT].

© Egor Dubenetskiy, 2019.

[ITMO University]: https://en.itmo.ru/
[Apache-2.0]: https://opensource.org/licenses/Apache-2.0
[MIT]: https://opensource.org/licenses/MIT
