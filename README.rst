===============================
assemble
===============================

.. image:: https://badge.fury.io/py/assemble.png
    :target: http://badge.fury.io/py/assemble

.. image:: https://travis-ci.org/kracekumar/assemble.png?branch=master
        :target: https://travis-ci.org/kracekumar/assemble

.. image:: https://pypip.in/d/assemble/badge.png
        :target: https://pypi.python.org/pypi/assemble


Make like build tool written in Python.

* How to use

- `assemble` . Looks for Assemblefile

::

   from assemble import task, sh


   @task(default=True)
   def clean():
        sh("find . -name '*.pyc' -exec rm -f {} +")
        sh("find . -name '*.pyo' -exec rm -f {} +")
        sh("find . -name '*~' -exec rm -f {} +")


   @task(default=True)
   def runserver():
       sh("workon myapp")
       sh("python manage.py runserver")


   @task
   def run_celery():
       sh("python manage.py celeryctl purge")
       sh("python manage.py celeryd")


   @task
   def grunt_init():
       sh("cd static/js/grunt && grunt")


   @task
   def grunt_watch():
       sh("cd static/js/grunt && grunt init")



::

   $assemble
   # Runs clean first and then runs runserver.


* Free software: BSD license
* Documentation: http://assemble.readthedocs.org.

* TODO
