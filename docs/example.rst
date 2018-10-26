ELIXIR API for REMS Examples
============================

The ELIXIR API consists of the following endpoints:

* ``/`` information endpoint;
* ``POST`` ``/user`` - Create new user with dataset permissions;
* ``GET`` ``/user/<username>`` - Get dataset permissions for <username>;
* ``PATCH`` ``/user/<username>`` - Create new dataset permissions for <username> (overwrites);
* ``DELETE`` ``/user/<username>`` - Delete <username> and dataset permissions;

For the full specification consult: `ELIXIR Permissions API specification <https://app.swaggerhub.com/apis-docs/ELIXIR-Finland/Permissions/1.2>`_.

Info Endpoint
-------------

.. code-block:: console

  $ curl -X GET 'http://localhost:8080/'

Example Response:

.. code-block:: javascript

  ELIXIR AAI API for REMS

User Endpoint
-------------

An example ``POST`` request and response to the ``user`` endpoint:

.. code-block:: console

  $ curl -X POST \
    http://localhost:8080/user \
    -H 'Content-Type: application/json' \
    -d '{
    "user_identifier": "test_user",
    "affiliation": "",
    "datasets": [
      {
        "permissions": [
          {
            "affiliation": "example-org",
            "source_signature": "",
            "url_prefix": "",
            "datasets": [
              "urn:example-dataset-1",
              "urn:example-dataset-2"
            ]
          }
        ]
      }
    ]
  }'

Example Response:

.. code-block:: javascript

  Successful operation

An example ``GET`` request and response to the ``user`` endpoint:

.. code-block:: console

  $ curl -X GET http://localhost:8080/user/test_user

Example Response:

.. code-block:: javascript

  {
    "permissions": [
        {
            "affiliation": "",
            "source_signature": "",
            "url_prefix": "",
            "datasets": [
                "urn:example-dataset-1",
                "urn:example-dataset-2"
            ]
        }
    ]
  }

An example ``PATCH`` request and response to the ``user`` endpoint:

.. code-block:: console

  $ curl -X PATCH \
    http://localhost:8080/user/test_user \
    -H 'Content-Type: application/json' \
    -d '{
    "user_identifier": "",
    "affiliation": "",
    "datasets": [
      {
        "permissions": [
          {
            "affiliation": "example-org",
            "source_signature": "",
            "url_prefix": "",
            "datasets": [
              "urn:example-dataset-3"
            ]
          }
        ]
      }
    ]
  }'

Example Response:

.. code-block:: javascript

  Successful operation

An example ``DELETE`` request and response to the ``user`` endpoint:

.. code-block:: console

  $ curl -X DELETE http://localhost:8080/user/test_user

Example Response:

.. code-block:: javascript

  User was deleted
