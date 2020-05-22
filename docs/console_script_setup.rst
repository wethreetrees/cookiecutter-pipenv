.. _console-script-setup:


Console Script Setup
=================

Optionally, your package can include a console script

How It Works
------------

# TODO

Usage
------------
To use the console script in development:

.. code-block:: bash

    $ cd projectdir
    $ pipenv install -e .

'projectdir' should be the top level project directory with the setup.py file

The script will be generated with output for no arguments and --help.

--help
    show help menu and exit

Known Issues
------------
Installing the project in a development environment using:

.. code-block:: bash

    $ python setup.py develop

will not set up the entry point correctly. This is a known issue with Click.
The following will work as expected:

.. code-block:: bash

    $ python setup.py install
    $ pip install mypackage

With 'mypackage' adjusted to the specific project.


More Details
------------

You can read more about Click at:
http://click.pocoo.org/
