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

This is currently still messed up and broken, requiring the containing directory to be executed as a module. Cloning this project into a repo called `newweb_info` would allow you to run it as `python -m newweb_info`. 