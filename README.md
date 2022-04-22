# pre-commit-cairo

[![Test and release](https://github.com/franalgaba/pre-commit-cairo/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/franalgaba/pre-commit-cairo/actions/workflows/release.yml)

Cairo hooks for pre-commit. See [pre-commit](https://github.com/pre-commit/pre-commit) for more details

## Using pre-commit-cairo with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/franalgaba/pre-commit-cairo
    rev: v0.0.1  # Use the ref you want to point at
    hooks:
    -   id: cairo-lint
```

## Hooks available

### `cairo-lint`

Checks lint of Cairo contracts using [Amarna](https://github.com/crytic/amarna).

Amarna does not have a public release yet. So, to use this hook your hook first you need to install Amarna in your project manually:

`pip install git+https://github.com/crytic/amarna.git@main`

or

`poetry add git+https://github.com/crytic/amarna.git@main`

After a public release for Amarna is made, the hook will install it automatically.