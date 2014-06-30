# -*- coding: utf-8 -*-

import os
import sys
import imp

from functools import wraps, partial

from envoy import run
import click

from variable import TASKS, DEFAULT_TASKS_KEY


def print_success_msg(msg):
    """Print message with green as foreground color.
    """
    click.secho(msg, fg='green')


def print_failure_msg(msg):
    """Print message with red as foreground color.
    """
    click.secho(msg, fg='red')


def task(func=None, *args, **kwargs):
    if not func:
        return partial(task, *args, **kwargs)

    try:
        name = kwargs.pop('name')
    except KeyError:
        name = func.__name__

    TASKS.update({name: func})

    if kwargs.get('default'):
        DEFAULT_TASKS_KEY.append(name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def sh(cmd, std_out=True):
    res = run(cmd)
    if res.status_code is 0:
        print_success_msg(res.std_out) if std_out else None
    else:
        print_failure_msg(res.std_err or res.std_out)
        print_failure_msg("Program exited with {}".format(res.status_code))
        exit()


def main():
    task_file = "Assemblefile"
    if not os.path.exists(task_file):
        print_failure_msg("{} file is missing".format(task_file))
        exit(127)

    load_file = imp.load_source('assemblefile', task_file)

    if len(sys.argv) == 1:
        for func in DEFAULT_TASKS_KEY:
            TASKS[func]()
    else:
        task_name = sys.argv[1]
        args = sys.argv[2:]
        try:
            TASKS[task_name](*args)
        except KeyError:
            print_failure_msg("Task {} doesn't exist".format(task_name))
