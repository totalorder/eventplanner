# Event Planner Pro 2005
Plan your events like there is no tomorrow!
 
# Development guide
EPP 2005 is written in Python with the web framework Django

## Installing Python
Download and install Python 2.7:
https://www.python.org/downloads/

## Getting the code
```bash
git clone https://github.com/totalorder/eventplanner.git
```

## Installing Python dependencies
Use `pip` to install the requirements listed in requirements.txt.

Optionally you can create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) 
and install the requirements in that.  
```bash
cd eventplanner/
pip install -r requirements.txt
```

## Running the tests
This should run all unit tests as well as the acceptance tests. 
The acceptance tests are run using [selenium](http://docs.seleniumhq.org/) which
runs a browser and executes commands and verifies the results automatically.
```bash
cd proj/
python manage.py test
```
Note: On windows you might see the error 
`Exception happened during processing of request from ('127.0.0.1', 60808)` 
when running the tests. 
This is not a problem, and as long as you see the output
`Ran 17 tests in 27.435s OK` everything worked.  

## Running the server
This starts a server on [http://localhost:8000/](http://localhost:5000/)

Login using any of usernames listed below, with the password `eventplanner`:

`cso` `scso` `fm` `adm` `psm` `hrm` 
```bash
python manage.py runserver
```