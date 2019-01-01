# nyc-top-airlines
Web app showing the most popular airlines in NYC airports. Running at https://nyctopairlines.pythonanywhere.com/

# Installation Instructions

This application is built using the Python [Flask 1.0](http://flask.pocoo.org/docs/1.0/) framework.  All requirements for the project can be installed using `pip install -r requirements.txt` using `requirements.txt` found in the root directory.  

The program is run using `flask run`.  To point Flask to the correct file, use `export FLASK_APP=app.py` ( or `set FLASK_APP=hello.py` on Windows). If you wish to run the app while in any directory, include the full path to app.py, such as `export FLASK_APP=~/Documents/myproject/app.py`

# Pushing Instructions

To create the `requirements.txt` (containing the necessary packages), run `pip freeze > requirements.txt` to overwrite the file in the root directory.  This is only necessary if packages have been updated.  
