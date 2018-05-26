# GImprove - Webserver

Landing Page and Prototype for Gimprove.

## Description
The program consists of two apps, `home` and `tracker`, which are both realized with the django-Framework:

### home
Responsible for the landing page. Handles the internationalization, the email-forms and the login.

### tracker
Responsible for the server-logic of the GImprove system. Includes a REST-API to retrieve, update, create and delete
data from the application.

## Usage
To run the application locally, execute `python3 manage.py runserver` from within the `sm_gym` directory. The app
will start to run under the following address: http://127.0.0.1:8000.

To test the tracker application, execute `python3 manage.py test tracker` from within the `sm_gym` directory.


## Contributing
**Dennis Meisner:** meisnerdennis@web.de

Find more detailed information in the Wiki.

#### Notes:

Create fixture for testing:
* Create user fixture: `python3 manage.py dumpdata auth.User --natural-foreign --indent=4>tracker/fixtures/auth.json`

* Create data fixture: `python3 manage.py dumpdata tracker --natural-foreign  --indent=4>tracker/fixtures/fix.json`

* Insert user-json into data fixture.
* There are errors when creating the fixture at the 'user'-attribute of the equipment-model. Correct by setting a single
number as value (number = user.pk).