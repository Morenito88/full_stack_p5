#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)

# Path to project wsgi
sys.path.insert(0,"/var/www/html/")

# Import the main application file
from full_stack_p3 import app as application

application.secret_key = 'cd48e1c22de0961d5d1bfb14f8a66e006cfb1cfbf3f0c0f3'
