web: gunicorn smartgym.wsgi --log-file -
web: daphne smartgym.asgi:application --port $PORT --bind 0.0.0.0
