"""WSGI script for Apache mod_wsgi

For more information about running and configuring mod_wsgi, please refer to
documentation at https://code.google.com/p/modwsgi/wiki/DeveloperGuidelines.
"""

# Assuming the project to run (and newWeb itself) are not installed system-wide,
# we will add the directories where they reside before we continue.
import os
import site
site.addsitedir('/path/to/env/lib/python2.7/site-packages')  # newWeb package
site.addsitedir(os.path.dirname(__file__))                   # info example

# Import the project and create a WSGI application object
import newweb_info
application = newweb_info.main()
