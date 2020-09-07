#!/bin/env/python

import os
from subprocess import call
import sys

# Run converalls command only on CI pipeline
# Solution provided by https://stackoverflow.com/questions/32757765/conditional-commands-in-tox-tox-travis-ci-and-coveralls

if __name__ == "__main__":
    if "COVERALLS_REPO_TOKEN" in os.environ:
        rc = call("coveralls")
        sys.stdout.write("Coveralls report\n")
    else:
        sys.stdout.write("Not on CI.\n")
