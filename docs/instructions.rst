Instructions
============

.. note:: This web server requires Python 3.6+ to run.

Environment Setup
-----------------

The application requires some environmental arguments in order to run properly, these are illustrated in
the table below.

+-------------+-------------------------------+-------------------------------------+
| ENV         | Default                       | Description                         |
+-------------+-------------------------------+-------------------------------------+
| `DB_HOST`   | `postgresql://localhost:5432` | The URL for the PostgreSQL server.  |
+-------------+-------------------------------+-------------------------------------+
| `DB_NAME`   | `rems`                        | Name of the database.               |
+-------------+-------------------------------+-------------------------------------+
| `DB_USER`   | `rems`                        | Database username.                  |
+-------------+-------------------------------+-------------------------------------+
| `DB_PASS`   | `rems`                        | Database password.                  |
+-------------+-------------------------------+-------------------------------------+
| `APP_HOST`  | `0.0.0.0`                     | Default Host for the Web Server.    |
+-------------+-------------------------------+-------------------------------------+
| `APP_PORT`  | `8080`                        | Default port for the Web Server.    |
+-------------+-------------------------------+-------------------------------------+
| `DEBUG`     | `True`                        | If set to `True`, logs all actions. |
+-------------+-------------------------------+-------------------------------------+

Setting the necessary environment variables can be done  e.g. via the command line:

.. code-block:: console

    $ export DB_HOST=postgresql://localhost:5432
    $ export DB_NAME=rems
    $ export DB_USER=rems
    $ export DB_PASS=rems
    $ export HOST=0.0.0.0
    $ export PORT=8080
    $ export DEBUG=True

.. _app-setup:

App Setup
-------------------

For installing `elixir-rems-proxy` do the following:

.. code-block:: console

    $ git clone https://github.com/CSCfi/elixir-rems-proxy
    $ pip install -r requirements.txt
    $ cd elixir-rems-proxy
    $ pip install .

To run the web app:

.. code-block:: console

    $ elixir_rems_proxy

.. _database-setup:

(Optional) Database Setup
-------------------------

If you are not connecting to an existing REMS database, but instead creating your own, an installation of PostgreSQL 9.6+ is required.

Setting up a REMS database and populating it with test data.

.. code-block:: console

    git clone https://github.com/CSCfi/rems/
    cd rems
    ./dev_db.sh
    lein run test-data

For more information regarding the REMS database, and in case of setup issues, consult https://github.com/CSCfi/rems/
