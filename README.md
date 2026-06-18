> [!IMPORTANT]
> This code was originally in a mono-repo with Aardvark, now being renamed to
> Exprés, but has been separated into a new repo. There may still be some
> mentions of Aardvark in the docs and code during the renaming/refactor.

> [!CAUTION]
> ASDF Qiskit is still a WIP and volatile. The library is primarily for personal
> use in our PhD research at IBM Research, Zürich, though anyone is welcome to
> use it. In its current state, it is not guaranteed that data saved with this
> version will be loadable in future versions, though we do aim for backwards
> compatibility during this time.

> [!IMPORTANT]
> Not all Qiskit objects are currently serialisable by ASDF Qiskit. For a
> complete list, see the supported types in the documentation.

## ASDF Qiskit

`asdf-qiskit` is an [ASDF](https://asdf.readthedocs.io/en/latest/) extension that
supports serialising [Qiskit](https://qiskit.org) objects into human-readable
YAML-like files. Our goal is to support most important Qiskit classes and data
containers, with backwards compatibility to load old experimental data with
newer versions of Qiskit and Python.

### Installation

In the near future, we will publish `asdf-qiskit` to PyPI. Until then, if you
would like to try `asdf-qiskit` you can run the command, below, and then use
ASDF as normal. **Note that the current version is 0.0.0. The first "release"
0.1.0 will occur very soon.**

```bash
pip install "git+ssh://git@github.com/conradhaupt/asdf-qiskit.git@main"
```

### Dependencies

`asdf-qiskit` requires Qiskit and ASDF. We enforce PyYAML versions greater than
6.0.2 to ensure compatibility with Python 3.13.

### Usage

As `asdf-qiskit` is an extension for ASDF, it is best to use their [overview
guide](https://www.asdf-format.org/projects/asdf/en/latest/asdf/overview.html).
The only change between their guide and usage with `asdf-qiskit` is that Qiskit
objects can now be saved and loaded with ASDF.

<!-- The following text should be added once the documentation is correctly hosted. -->
<!-- See [the supported-types docs page](#to_be_completed). -->
<!-- For an explicit list of common yet unsupported types, see the [unsupported-types docs page](#to_be_completed). -->

## Documentation

The documentation will be hosted with Github pages soon. As the code progresses,
the documentation will be updated. The most up-to-date and extensive parts of
the docs are the guides.

# Contributing

All contributions are welcome. If you would like to test the library or
contribute more regularly, please talk to either Conrad Haupt (@conradhaupt) or
Marc Drudis (@MarcDrudis).
