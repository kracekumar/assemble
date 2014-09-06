### assemble

- Make like build tool written in Python.

#### How to use

- `assemble` command, looks for Assemblefile in the current directory.

```

    #!/usr/bin/env assemble

    from assemble import task, sh

    # Random tasks for testing

    @task(default=True)
    def echo():
    """Default
    """
    sh("echo default")


    @task
    def name(*args):
    sh("echo {}".format(' '.join(args)))


    @task
    def df():
    sh("df -h")


    # Useful tasks
    @task
    def cleanpyc():
    """Remove all pyc in the current project.
    """
    sh('find . -name "*.pyc" -exec rm -rf {} \;')
    sh('find . -name "*.pyo" -exec rm -f {} +')
    sh('find . -name "*~" -exec rm -f {} +')


    @task
    def clean_build():
    """Remove build, dist, *egg.info directories
    """
    sh('rm -fr build/')
    sh('rm -fr dist/')
    sh('rm -fr *.egg-info')


    @task
    def clean_pyc():
    cleanpyc()


    @task
    def clean():
    """cleans *.py[co] files and build, dist, *.egg-info directories
    """
    clean_build()
    cleanpyc()


    @task
    def coverage():
    """Run all test using coverage and open the coverage report
    """
    sh('tox')
    sh('open htmlcov/index.html')


    @task
    def release():
    """Upload the code to pypi.
    """
    sh('python setup.py sdist upload')
    sh('python setup.py bdist_wheel upload')


    @task
    def dist():
    sh('python setup.py sdist')
    sh('python setup.py bdist_wheel')
    sh('ls -l dist')


    @task
    def test():
    """Run all test cases in different python version"""
    test_all()


    @task
    def test_all():
    """Run all test cases in different python version"""
    sh('tox')
```

```bash
    assemble $ assemble --help
    Usage: assemble [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    clean        cleans *.
    clean_build  Remove build, dist, *egg.
    clean_pyc
    cleanpyc     Remove all pyc in the current project.
    coverage     Run all test using coverage and open the...
    df
    dist
    echo         Default
    name
    release      Upload the code to pypi.
    test         Run all test cases in different python...
    test_all     Run all test cases in different python...
    assemble $ assemble
    default

    assemble $

```

#### Install

- `pip install -e git+https://github.com/kracekumar/assemble\#egg\=assemble`

#### Development

- `$pip install -r dev_requirements.txt`

#### Testing
- `$tox`


Test coverage is 96%.

- Free software: BSD license

#### TODO

  - Documentation: http://assemble.readthedocs.org.
  - Distribute in PyPi.
  - Add `circleci` support.
