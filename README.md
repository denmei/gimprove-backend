# GImprove - Webserver

Landing Page and Prototype for Gimprove.

#### Notes:

Create fixture for testing:
* Create user fixture: `python3 manage.py dumpdata auth.User --natural-foreign --indent=4>tracker/fixtures/auth.json`

* Create data fixture: `python3 manage.py dumpdata tracker --natural-foreign  --indent=4>tracker/fixtures/fix.json`

* Insert user-json into data fixture.