#!/usr/bin/env python3

from flask import Flask, request, abort, jsonify
import os
import logging

# Logging
FORMAT = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

app = Flask(__name__)


@app.route('/')
def hello():
    """Health check."""
    return 'REMS Mock API'


@app.route('/api/entitlements')
def api_endpoint():
    """
    Request endpoint, simulates REMS API.

    Required headers:
        x-rems-api-key
        x-rems-user-id
    """
    # Check that headers were received
    LOG.info(request.headers)

    # Validate headers
    if request.headers['X-Rems-Api-Key'] != os.environ.get('REMS_API_KEY', 'abc123'):
        return abort(401, 'API key rejected.')
    if request.headers['X-Rems-User-Id'] != os.environ.get('REMS_USER_ID', 'userid@elixir-europe.org'):
        return abort(404, 'User not found.')

    return jsonify([{"resource": "EGAD000000001",
                     "application-id": 100001,
                     "start": "01-01-2018",
                     "mail": "dac1@owner.org"},
                    {"resource": "EGAD000000002",
                     "application-id": 100002,
                     "start": "05-05-2018",
                     "mail": "dac2@owner.org"}])


def main():
    """Run mock app."""
    app.run(host=os.environ.get('APP_HOST', 'localhost'),
            port=os.environ.get('APP_PORT', 5000),
            debug=os.environ.get('APP_DEBUG', True))


if __name__ == '__main__':
    main()
