# Boto3 Stubs Package

> Auto-generated documentation for [mypy_boto3_builder.writers.boto3_stubs_package](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/writers/boto3_stubs_package.py) module.

boto3-stubs package writer.

- [mypy-boto3-builder](../../README.md#mypy_boto3_builder) / [Modules](../../MODULES.md#mypy-boto3-builder-modules) / [Mypy Boto3 Builder](../index.md#mypy-boto3-builder) / [Writers](index.md#writers) / Boto3 Stubs Package
    - [write_boto3_stubs_docs](#write_boto3_stubs_docs)
    - [write_boto3_stubs_package](#write_boto3_stubs_package)

## write_boto3_stubs_docs

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/writers/boto3_stubs_package.py#L93)

```python
def write_boto3_stubs_docs(
    package: Boto3StubsPackage,
    output_path: Path,
) -> None:
```

Generate docs for boto3-stubs package.

#### See also

- [Boto3StubsPackage](../structures/boto3_stubs_package.md#boto3stubspackage)

## write_boto3_stubs_package

[[find in source code]](https://github.com/vemel/mypy_boto3_builder/blob/master/mypy_boto3_builder/writers/boto3_stubs_package.py#L21)

```python
def write_boto3_stubs_package(
    package: Boto3StubsPackage,
    output_path: Path,
    generate_setup: bool,
) -> None:
```

Generate stubs for boto3-stubs package.

#### See also

- [Boto3StubsPackage](../structures/boto3_stubs_package.md#boto3stubspackage)
