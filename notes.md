# Notes

## Create fixture for testing:
* Create user fixture: `python3 manage.py dumpdata auth.User --natural-foreign --indent=4>tracker/fixtures/auth.json`

* Create data fixture: `python3 manage.py dumpdata tracker --natural-foreign  --indent=4>tracker/fixtures/fix.json`

* Insert user-json into data fixture.
* There are errors when creating the fixture at the 'user'-attribute of the equipment-model. Correct by setting a single
number as value (number = user.pk).