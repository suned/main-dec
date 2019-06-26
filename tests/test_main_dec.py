import inspect
import sys
from argparse import Namespace
import typing as t
from enum import Enum

import pytest

from main_dec import _create_parser, main


def test_non_annotated_no_default():
    def f(required):
        pass

    parser = _create_parser(f)
    assert parser.parse_args(['']) == Namespace(required='')


def test_annotated():
    def f(required: int):
        pass

    parser = _create_parser(f)
    assert parser.parse_args(['0']) == Namespace(required=0)


def test_default():
    def f(optional=0):
        pass

    parser = _create_parser(f)
    assert parser.parse_args([]) == Namespace(optional=0)
    assert parser.parse_args('--optional 1'.split()) == Namespace(optional=1)


def test_annotated_default():
    def f(optional: int = 0):
        pass

    parser = _create_parser(f)
    assert parser.parse_args([]) == Namespace(optional=0)
    assert parser.parse_args('--optional 1'.split()) == Namespace(optional=1)


def test_list_annotated():
    def f(required: t.List):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2 3'.split())
    assert actual == Namespace(required=['1', '2', '3'])


def test_list_annotated_with_type_arg():
    def f(required: t.List[int]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2 3'.split())
    assert actual == Namespace(required=[1, 2, 3])


def test_builtin_list_annotated():
    def f(required: list):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2 3'.split())
    assert actual == Namespace(required=['1', '2', '3'])


def test_list_default():
    def f(optional=[]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--optional 1 2 3'.split())
    assert actual == Namespace(optional=['1', '2', '3'])


def test_list_default_with_type():
    def f(optional=[1]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--optional 1 2'.split())
    assert actual == Namespace(optional=[1, 2])


def test_tuple_annotated():
    def f(required: t.Tuple):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2'.split())
    assert actual == Namespace(required=('1', '2'))


def test_tuple_annotated_with_type_arg():
    def f(required: t.Tuple[int, str]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2'.split())
    assert actual == Namespace(required=(1, '2'))

    with pytest.raises(SystemExit):
        parser.parse_args('1'.split())

    with pytest.raises(SystemExit):
        parser.parse_args('1 2 3'.split())


def test_tuple_with_ellipsis():
    def f(required: t.Tuple[int, ...]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2 3'.split())
    assert actual == Namespace(required=(1, 2, 3))


def test_builtin_tuple_annotated():
    def f(required: tuple):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('1 2'.split())
    assert actual == Namespace(required=('1', '2'))


def test_tuple_default():
    def f(optional=()):
        pass

    parser = _create_parser(f)
    assert parser.parse_args('--optional 1'.split()) == Namespace(optional=('1',))


def test_tuple_default_with_type():
    def f(optional=(1,)):
        pass

    parser = _create_parser(f)
    assert parser.parse_args('--optional 1 2 3'.split()) == Namespace(optional=(1, 2, 3))


def test_tuple_default_with_more_than_one_type():
    def f(optional=(1, '2')):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--optional 3 4'.split())
    assert actual == Namespace(optional=(3, '4'))


def test_positive_flag():
    def f(flag=False):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--flag'.split())
    assert actual == Namespace(flag=True)


def test_negative_flag():
    def f(flag=True):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--flag'.split())
    assert actual == Namespace(flag=False)


def test_optional_snake():
    def f(snake_cased=''):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--snake-cased test'.split())
    assert actual == Namespace(snake_cased='test')


class Choice(Enum):
    first = 1
    second = 2


def test_choices_annotation():
    def f(required: Choice):
        pass

    parser = _create_parser(f)

    with pytest.raises(SystemExit):
        parser.parse_args('third'.split())

    actual = parser.parse_args('first'.split())
    assert actual == Namespace(required=Choice.first)


def test_choices_default():
    def f(optional=Choice.first):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--optional second'.split())
    assert actual == Namespace(optional=Choice.second)
    assert parser.parse_args([]) == Namespace(optional=Choice.first)


def test_list_annotated_choice():
    def f(required: t.List[Choice]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('first first second'.split())
    assert actual == Namespace(required=[Choice.first, Choice.first, Choice.second])


def test_list_default_choice():
    def f(optional=[Choice.first]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--optional first second'.split())
    assert actual == Namespace(optional=[Choice.first, Choice.second])


def test_tuple_choice_annotated():
    def f(required: t.Tuple[Choice, Choice]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('first first'.split())
    assert actual == Namespace(required=(Choice.first, Choice.first))


def test_tuple_choice_annotated_ellipsis():
    def f(required: t.Tuple[Choice, ...]):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('first first second'.split())
    assert actual == Namespace(required=(Choice.first, Choice.first, Choice.second))


def test_tuple_choice_default():
    def f(optional=(Choice.first,)):
        pass

    parser = _create_parser(f)
    actual = parser.parse_args('--optional first second'.split())
    assert actual == Namespace(optional=(Choice.first, Choice.second))


def test_rest_help():
    def f(required, required_str: str, optional=1):
        """
        A small function to test that help is generated correctly

        :param required: A required parameter
        :param required_str: A required str parameter
        :param optional: An optional parameter
        :return:
        """

    parser = _create_parser(f)
    actual = parser.format_help()
    expected = '''
    usage: test_main_dec [-h] [--optional OPTIONAL] required required_str

    A small function to test that help is generated correctly

    positional arguments:
      required             A required parameter
      required_str         A required str parameter

    optional arguments:
      -h, --help           show this help message and exit
      --optional OPTIONAL  An optional parameter
    '''

    assert actual == inspect.cleandoc(expected) + '\n'


def test_google_help():
    def f(required, optional=''):
        """
        A small function to test that help is generated correctly

        Args:
            required (str): A required parameter
            optional (str): An optional parameter
        """

    parser = _create_parser(f)
    actual = parser.format_help()
    expected = '''
    usage: test_main_dec [-h] [--optional OPTIONAL] required

    A small function to test that help is generated correctly

    positional arguments:
      required             A required parameter

    optional arguments:
      -h, --help           show this help message and exit
      --optional OPTIONAL  An optional parameter
    '''

    assert actual == inspect.cleandoc(expected) + '\n'


def test_main():
    def f(required):
        assert required == 'arg'

    f.__module__ = '__main__'
    with pytest.raises(SystemExit):
        main(f)
    sys.argv = 'command arg'.split()
    main(f)
