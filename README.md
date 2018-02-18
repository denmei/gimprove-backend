python3 manage.py dumpdata auth.User --natural-foreign --indent=4>tracker/fixtures/auth.json
python3 manage.py dumpdata tracker --natural-foreign  --indent=4>tracker/fixtures/fix.json