## ELIXIR API for REMS
This API is built according to the [ELIXIR Permissions API Specification 1.2](https://app.swaggerhub.com/apis-docs/ELIXIR-Finland/Permissions/1.2), which provides ELIXIR AAI with a custom API that is directly connected to a given REMS database.

### Quickstart
#### Prerequisites
Set up a REMS database with test data.
```
git clone https://github.com/CSCfi/rems/
cd rems
./dev_db.sh
lein run test-data
```
In case of issues with setting up the REMS database, consult their [GitHub page](https://github.com/CSCfi/rems/).

#### Run API
Download repository, install modules, run app.
```
git clone https://github.com/CSCfi/elixir-rems-proxy/
cd elixir-rems-proxy
pip install -r requirements.txt
python3 -m api.app
```

### Using the API
For more technical details, consult the [API Specification](https://app.swaggerhub.com/apis-docs/ELIXIR-Finland/Permissions/1.2)

#### POST /user
`POST` method at `/user` endpoint is used to create a new user with dataset permissions.
```
curl -X POST \
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
```

#### GET /user/username
`GET` method at `/user` endpoint is used to fetch dataset permissions for user.
```
curl -X GET http://localhost:8080/user/test_user
```

#### PATCH /user/username
`PATCH` method at `/user` endpoint is used to update dataset permissions for user.
```
curl -X PATCH \
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
```

#### DELETE /user/username
`DELETE` method at `/user` endpoint is used to delete user along with dataset permissions.
```
curl -X DELETE http://localhost:8080/user/teemu2
```

### Other Business
The [Permissions API Specification](https://app.swaggerhub.com/apis-docs/ELIXIR-Finland/Permissions/1.2) contains some typos. A [suggestions](suggestions.md) document has been drafted to correct those issues. Expect changes to be made to the specification in the near future, along with changes to the API app.
