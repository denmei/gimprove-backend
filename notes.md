# Notes

## Create fixture for testing:
* Create user fixture: `python3 manage.py dumpdata auth.User --natural-foreign --indent=4>fixtures/auth.json`

* Create tracker fixture: `python3 manage.py dumpdata tracker --natural-foreign  --indent=4>fixtures/tracker.json`

* Create main fixture: ` python3 manage.py dumpdata main --natural-foreign  --indent=4>fixtures/main.json
`
* Insert user-json into data fixture.
* There are errors when creating the fixture at the 'user'-attribute of the equipment-model. Correct by setting a single
number as value (number = user.pk).