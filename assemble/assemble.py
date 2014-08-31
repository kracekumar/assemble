# -*- coding: utf-8 -*-

import os
import sys
import imp
import inspect

from functools import wraps, partial

from envoy import run
import click

from variable import DEFAULT_TASKS_KEY, TASKS_WITH_ARGS


def print_success_msg(msg):
    """Print message with green as foreground color.
    """
    click.secho(msg, fg='green', file=sys.stdout)


def print_failure_msg(msg):
    """Print message with red as foreground color.
    """
    click.secho(msg, fg='red', file=sys.stderr)


# This required to register other commands
@click.group()
@click.pass_context
def cli(ctx, verbose=True):
    pass


def is_args_in_task(func):
    """Check if func.func_code has *args.

    @aparm func: function reference
    """
    arg = inspect.getargs(func.func_code)
    return arg.varargs is not None


def add_task(name, func, help, is_default=False):
    """Add a task to default `click.Group`.

    @param name `string`: Name of the task.
    @param func `string`: Function reference to the task.
    @param help `string`: function help text. Mostly __doc__ of the function.
    @param is_default `bool`: Is this task default.
    """
    cmd = click.Command(name=name, callback=func, help=help)
    cli.add_command(cmd)

    if is_default:
        # Store all functions here without name.
        DEFAULT_TASKS_KEY.append(func)

    return cli


def task(func=None, *args, **kwargs):
    """Decorator to make any python function task.

    @task
    def foo():
        print "foo"

    @task(default=True)
    def ls():
        sh("ls -laR")

    @task
    def clean(*args):
        # assemble clean pyc pyx pyo
        files = os.listdir('.')
        for file in files:
            if file.endswith(args):
                os.remove(file)
    """
    if not func:
        return partial(task, *args, **kwargs)

    try:
        name = kwargs.pop('name').lower()
    except KeyError:
        name = func.__name__.lower()

    # Extract docs for the given func
    help = inspect.getdoc(func)
    add_task(name, func, help, kwargs.get('default'))

    # If task has args store it in TASK_WITH_ARGS
    # Todo: Move this logic also to `click`

    if is_args_in_task(func):
        TASKS_WITH_ARGS.add(name)

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
        exit(res.status_code)


def load_assemble_file(task_file):
    """Load the task file. By loading the file we register all the tasks.

    @param task_file: Full path of the file or filename in current directory.
    """
    return imp.load_source('assemblefile', task_file)


def check_for_assemble_file(task_file):
    """Check for assemblie file in the current directory.
    If file is missing exit with status code 127.

    @param task_file, string: Assemblefile name or full path.
    """
    if not os.path.exists(task_file):
        print_failure_msg("{} file is missing".format(task_file))
        exit(127)
    return True


def run_func_from_click_group(click_group, command_name, *args):
    """Run the command registered in the click group.

    @param click_group: `click.Group` object which has all commands registered.
    @param command_name: Name of the task name.
    """
    # Pass empty context
    cmd = click_group.get_command({}, command_name)
    if cmd:
        res = cmd.callback(*args)
        return res or True


def run_all_default_tasks():
    """Run all the default tasks
    """
    for func in DEFAULT_TASKS_KEY:
        func()


def main(argv=None):
    task_file = 'Assemblefile'

    check_for_assemble_file(task_file)

    load_assemble_file(task_file)

    argv = argv or sys.argv

    if len(argv) == 1:
        run_all_default_tasks()
    else:
        task_name = argv[1].lower()
        args = argv[2:]

        # Making in operation O(1)
        if '--help' in set(argv):
            cli([task_name].extend(args))

        res = run_func_from_click_group(cli, task_name, *args)
        if not res:
            print_failure_msg("{} task not found".format(task_name))
            sys.exit(2)
