# GImprove - Webserver

Landing Page and Prototype for Gimprove.

## Description
The program consists of two apps, `landing_page` and `tracker`, which are both realized with the django-Framework:

### landing_page
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