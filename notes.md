# Notes

## Create fixture for testing:
* Create user fixture: `python3 manage.py dumpdata auth.User --natural-foreign --indent=4>fixtures/auth.json`
* Create tracker fixture: `python3 manage.py dumpdata app_tracker --natural-foreign  --indent=4>fixtures/tracker.json`
* Create main fixture: `python3 manage.py dumpdata app_main --natural-foreign  --indent=4>fixtures/main.json`
* Create network fixture: `python3 manage.py dumpdata app_network --natural-foreign  --indent=4>fixtures/network.json`
* Create achievement fixture: `python3 manage.py dumpdata app_achievements --natural-foreign  --indent=4>fixtures/achievements.json`

* Copy content of all files into one file and name it 'fix.json'
* There are errors when creating the fixture at the 'user'-attribute of the equipment-model. Correct by setting a single
number as value (number = user.pk).