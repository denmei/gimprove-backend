import os

os.system("python3 manage.py dumpdata auth.User --natural-foreign --indent=4>fixtures/auth.json")
os.system("python3 manage.py dumpdata app_tracker --natural-foreign --indent=4>fixtures/tracker.json")
os.system("python3 manage.py dumpdata app_main --natural-foreign --indent=4>fixtures/main.json")
os.system("python3 manage.py dumpdata app_network --natural-foreign --indent=4>fixtures/network.json")
os.system("python3 manage.py dumpdata app_achievements --natural-foreign --indent=4>fixtures/achievements.json")
