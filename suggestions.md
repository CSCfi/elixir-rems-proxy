#### Suggestions for the ELIXIR Permissions API Specification
The [Permissions API Specification](https://app.swaggerhub.com/apis-docs/ELIXIR-Finland/Permissions/1.2) has some minor flaws, which this document aims to correct.

### POST /user

#### Payload
The `POST` method at `/user` endpoint has an extra `datasets` branch in the JSON payload.

Current format:
```
{
  "user_identifier": "string",
  "affiliation": "string",
  "datasets": [
    {
      "permissions": [
        {
          "affiliation": "user@example.com",
          "source_signature": "string",
          "url_prefix": "string",
          "datasets": [
            "string"
          ]
        }
      ]
    }
  ]
}
```

Suggested format:
```
{
  "user_identifier": "string",
  "affiliation": "string",
  "permissions": [
    {
      "affiliation": "user@example.com",
      "source_signature": "string",
      "url_prefix": "string",
      "datasets": [
        "string"
      ]
    }
  ]
}
```

#### Responses
The `POST` method at `/user` endpoint has the following response specified:

| Code | Description |
| --- | --- |
| default | Successful operation |

Suggested responses:

| Code | Description |
| --- | --- |
| 200 | Successful operation |
| 201 | Partially successful operation (something was done, something was not done, usually happens when user is attempting to add permissions to datasets which don't exist in REMS. Response body can return the missing datasets which were in the request, see [app.py return http response](/api/app.py#L38).) |
| 409 | Username is taken |

### GET /user/username

#### Query Parameter
The `GET` method at `/user/username` endpoint has an optional query parameter `user_affiliation` which can't be tied to any item in the REMS database. As such, this parameter can't be leveraged with the current REMS database schema. The only thing that might indicate a user's affiliation is in the `user` -table's `userattrs` column, which is an email-address embedded within a jsonb: `{"eppn": "user_id", "mail": "user_id@org.org", "commonName": "User Name"}`. Attempting to parse this from all users could prove to be an expensive operation.

#### Responses
The `GET` method at `/user/username` endpoint already has response codes `200` and `404` for `Successful operation` and `User not found` respectively.

Suggested response addition:

| Code | Description |
| --- | --- |
| 400 | Invalid username / Missing mandatory parameter username |

### PATCH /user/username
#### Payload
The `PATCH` method at `/user/username` is decribed as a `PUT` method.

The JSON payload for `PATCH` is identical to that of the `POST` endpoint, currently:
```
{
  "user_identifier": "string",
  "affiliation": "string",
  "datasets": [
    {
      "permissions": [
        {
          "affiliation": "user@example.com",
          "source_signature": "string",
          "url_prefix": "string",
          "datasets": [
            "string"
          ]
        }
      ]
    }
  ]
}
```
But this means the endpoint should in fact be a `PUT` method, because the endpoint is used to do a full replacement of data. To conform the endpoint to `PATCH` method standards, only the item that will be changed should be specified.

Suggested payload format:
```
{
  "permissions": [
    {
      "affiliation": "user@example.com",
      "source_signature": "string",
      "url_prefix": "string",
      "datasets": [
        "string"
      ]
    }
  ]
}
```

#### Responses
The `PATCH` method at `/user/username` endpoint has the following response specified:

| Code | Description |
| --- | --- |
| default | Successful operation |

Suggested responses:

| Code | Description |
| --- | --- |
| 200 | Successful operation |
| 201 | Partially successful operation (something was done, something was not done, usually happens when user is attempting to add permissions to datasets which don't exist in REMS. Response body can return the missing datasets which were in the request, see [app.py return http response](/api/app.py#L86).) |
| 400 | Invalid username / Missing mandatory parameter username |
| 404 | User not found |

### DELETE /user/username
No suggestions for this endpoint.
