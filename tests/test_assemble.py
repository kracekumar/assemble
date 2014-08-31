#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_assemble
----------------------------------

Tests for `assemble` module.
"""
from types import ModuleType

import pytest

from assemble import assemble


def test_cli_with_existing_command():
    with pytest.raises(SystemExit) as exc:
        assemble.cli(["--help"])
    # Since --help will always pass
    assert exc.value.code == 0


def test_cli_with_missing_command():
    with pytest.raises(SystemExit) as exc:
        assemble.cli(["-help"])
    # Since -help will be missing
    assert exc.value.code == 2


def test_sh_for_success_msg():
    assert assemble.sh("ls -la") is None


def test_sh_raises_exit_code_127():
    with pytest.raises(SystemExit) as exc:
        assemble.sh("foo")

    assert exc.value.code == 127


def test_sh_raises_systemexit():
    with pytest.raises(SystemExit) as exc:
        assert assemble.sh("cp foo.py foo1.py")


def test_load_assembile_file_from_current_directory():
    result = assemble.load_assemble_file("Assemblefile")
    assert isinstance(result, ModuleType)


def test_load_assembile_file_from_tests_directory():
    with pytest.raises(IOError):
        assert isinstance(assemble.load_assemble_file("tests/Assemblefile"),
                          ModuleType)


def test_check_for_assemble_file_in_base_directory():
    assert assemble.check_for_assemble_file('Assemblefile')


def test_check_for_assemble_file_in_tests_directory():
    with pytest.raises(SystemExit) as exc:
        assemble.check_for_assemble_file('test/Assemblefile')

    assert exc.value.code == 127


def test_is_args_in_task_without_args():
    def inner():
        pass

    assert assemble.is_args_in_task(inner) is False


def test_is_args_in_task_with_args():
    def inner(*args):
        pass

    assert assemble.is_args_in_task(inner) is True


def test_add_task_without_default():
    def inner():
        pass

    name = inner.__name__
    result = assemble.add_task(name=name, func=inner, help="inner")
    assert name in result.commands


def test_add_task_with_default():
    def inner():
        pass

    name = inner.__name__
    result = assemble.add_task(name=name, func=inner, help="inner",
                               is_default=True)
    assert name in result.commands
    assert inner in assemble.DEFAULT_TASKS_KEY


def test_run_func_from_click_group_when_func_exists():
    def inner():
        return 2

    name = inner.__name__
    click_group = assemble.add_task(name, inner, "help")
    assert assemble.run_func_from_click_group(click_group, name) == 2


def test_run_func_from_click_group_when_func_missing():
    def inner():
        return 2

    name = "foo"
    click_group = assemble.add_task(name, inner, "help")
    assert assemble.run_func_from_click_group(click_group, "me") is None


# Integration test
def test_main_for_default_case(capfd):
    argv = ["/usr/local/bin/assemble"]
    assemble.main(argv)

    out, err = capfd.readouterr()
    assert "default" in out


def test_main_for_task_with_args(capfd):
    argv = ["/usr/local/bin/assemble", "name", "python"]
    assemble.main(argv)

    out, err = capfd.readouterr()
    assert "python" in out


def test_main_when_task_is_missing():
    argv = ["/usr/local/bin/assemble", "bang"]
    with pytest.raises(SystemExit) as exc:
        assemble.main(argv)

    assert exc.value.code == 2

# def test_main_for_help_case(capfd):
#     argv = ["/usr/local/bin/assemble", "--help"]
#     assemble.main(argv)

#     out, err = capfd.readouterr()
#     assert "default" in out
