#!/usr/bin/python
import sys
import os
import logging
logging.basicConfig(stream=sys.stderr)

# Add project directory to sys.path
sys.path.insert(0, "/var/www/irismlapi/flask_iris/src/")

# Import your Flask app (adjust the module name if needed)
from app import app as application
