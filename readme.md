# newWeb example

This is an example web application that demonstrates some of the core functionality of [newWeb](/edelooff/newWeb). The main page shows a listing of query paramters, POST data and provided cookies and allows the user to set their own POST data and/or cookies. Additionally, a full listing of environment variables is included.

Code-wise, it showcases the following:

* request routing and server setup
* use of PageMaker, and Page classes (in `pages.py`);
* use of the templateparser (in `pages.py`) and templates (in `templates/*`).

It doesn't demonstrate any of the following:

* Configuration files and automatic parsing thereof;
* Database connectivity.


# How to run

Simply running the `serve.py` script included at the repository root should suffice, assuming newWeb itself has been installed. Additionally, an Apache configuration and WSGI script are included, allowing for migration from `mod_python` (µWeb) to `mod_wsgi` (newWeb).