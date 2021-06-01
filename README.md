# Agent Testing Demonstration

This repository demonstrates testing an agent by exercising its protocols from
the outside using pytest.

## Quickstart

Install poetry locally or globally:

#### Local

```sh
$ python3 -m venv env
$ source env/bin/activate
$ pip install poetry
```

#### Global

```sh
$ pip install --user poetry
```

Install dependencies:

```sh
$ poetry install
```

Run tests with:

```sh
$ poetry run pytest
```

## Contributing

### Pre-Commit

This project uses pre-commit to help developers maintain consistency in their
code. It is strongly encouraged that you use install these hooks.


Install pre-commit hooks (after `poetry install`):

```sh
$ pre-commit install --hook-type commit-msg
$ pre-commit install
```

### Conventional Commits

This project uses [conventional
commit](https://www.conventionalcommits.org/en/v1.0.0-beta.2/) messages. It is
strongly recommended that all contributions follow this standard for commit
messages. Commit early and often!
