# `main_dec`

A small library for painless commandline argument parsing in python.
## Install

`> pip install main-dec`

## Quickstart
```python
# my_cli.py

from typing import Tuple

from main_dec import main


@main
def run(required_str: str, optional_int=1, optional_tuple: Tuple[int, ...]=()):
    """
    A small example cli
    
    :param required_str: a required str
    :param optional_int: an optional int
    :param optional_tuple: an optional tuple
    """
    print('required_str', required_str)
    print('optional_int', optional_int)
    print('optional_tuple', optional_tuple)
```

```console
> python -m my_cli -h
usage: my_cli [-h] [--optional-tuple OPTIONAL_TUPLE [OPTIONAL_TUPLE ...]] [--optional-int OPTIONAL_INT] required_str

A small example cli

positional arguments:
  required_str          a required str

optional arguments:
  -h, --help            show this help message and exit
  --optional-tuple OPTIONAL_TUPLE [OPTIONAL_TUPLE ...]
                        an optional tuple
  --optional-int OPTIONAL_INT
                        an optional int

> python -m my_cli arg --optional-int 2 --optional-tuple 1 2 3
required_str arg
optional_int 2
optional_tuple (1, 2, 3)
```

## Required and optional arguments

Positional arguments to your function will be parsed as required arguments to your cli.
Optional arguments to your function will be parsed as optional arguments.
```python
# my_cli.py

from main_dec import main


@main
def run(required_arg: str, optional_arg=''):
    pass
```

```console
> python -m my_cli -h
usage: my_cli [-h] [--optional-arg OPTIONAL_ARG] required_arg

positional arguments:
  required_arg

optional arguments:
  -h, --help            show this help message and exit
  --optional-arg
```

## Flags
Optional `bool` arguments are parsed as flags, such that passing them
on the commandline "flips" their
truthiness.

```python
# my_cli.py

from main_dec import main

@main
def run(positive_flag=False, negative_flag=True):
    print('positive_flag', positive_flag)
    print('negative_flag', negative_flag)
```
```console
> python -m my_cli --postive-flag --negative-flag
positive_flag True
negative_flag False
```
## Type conversions
PEP484 annotated arguments and arguments with default values will have their
types converted before they are passed to your function.
```python
# my_cli.py

from typing import Tuple 

from main_dec import main


@main
def run(required_float: float, optional_tuple: Tuple[float, ...] = ()):
    print('required_float', required_float)
    print('optional_tuple', optional_tuple)
```
```console
> python -m my_cli 1 --optional-tuple 2 3 4
required_float 1.0
optional_tuple (2.0, 3.0, 4.0)
```
Currently supported types are `str`, `bytes`, `int`, `float`, `list` (including `typing.List`), `tuple` 
(including `typing.Tuple`) and `Enum`. `str` is the default type
for arguments that are not annotated and do not have a default value.
## Tuple arguments
Tuple arguments can either be parsed as varied length tuples, or fixed length tuples.

Fixed length tuples are arguments that are annotated without `...` as a type variable,
or arguments with default values with mixed types

```python
# my_cli.py

from typing import Tuple

from main_dec import main


@main
def run(fixed_length_tuple1: Tuple[int, int], fixed_length_tuple2=(1, 'arg')):
    pass
```

```console
> python -m my_cli -h
usage: my_cli [-h] [--fixed-length-tuple2 FIXED_LENGTH_TUPLE2 FIXED_LENGTH_TUPLE2] fixed_length_tuple1 fixed_length_tuple1

positional arguments:
  fixed_length_tuple1

optional arguments:
  -h, --help            show this help message and exit
  --fixed-length-tuple2 FIXED_LENGTH_TUPLE2 FIXED_LENGTH_TUPLE2
```

Varied length tuples are arguments that

- Are annotated with `...` as a type variable (e.g `Tuple[int, ...]`)
- Are annotated simply with `Tuple` or `tuple`
- Have a tuple as a default value with homogeneous types (e.g `(1, 2)`)
## Enum arguments
Arguments annotated with`Enum`, or with a default `Enum` type, can be used
to enforce that an argument must have certain values.

```python
# my_cli.py

from enum import Enum

from main_dec import main

class Choice(Enum):
    first = 1
    second = 2

@main
def run(argument_with_choices: Choice):
    print('argument_with_choices', argument_with_choices)
```
```console
> python -b my_cli -h
usage: my_cli [-h] {first,second}

positional arguments:
  {first,second}

optional arguments:
  -h, --help      show this help message and exit
 
> python -m my_cli second
argument_with_choices Choice.second
```

This can be combined with generic types such as `typing.Tuple` and `typing.List`, as well
as arguments with default arguments that are `tuple` or `list` types with `Enum` elements. 

## CLI Documentation
Doc strings in ReST or Google style are parsed and used to create usage
and help messages
```python
# my_cli.py

from main_dec import main

@main
def run(arg: str):
    """
    An example cli
    
    :param arg: A required argument
    """
```

```console
> python -m my_cli -h
usage: my_cli [-h] arg

An example cli

positional arguments:
  arg         A required argument

optional arguments:
  -h, --help  show this help message and exit
```